import functools
import queue
import threading
import time
from typing import Any, Callable, List, TypedDict

from django.db import transaction
from requests.auth import HTTPBasicAuth
from requests.sessions import Session

from doge_client.main import DogeClient
from doge_indexer.models import (
    DogeBlock,
    DogeTransaction,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)
from doge_indexer.models.types import IUtxoVinTransaction
from configuration.config import config


class BlockProcessorMemory(TypedDict):
    tx: List[DogeTransaction]
    vins: List[TransactionInput]
    vins_cb: List[TransactionInputCoinbase]
    vouts: List[TransactionOutput]


class BlockInformationPassing(TypedDict):
    block_num: int
    block_ts: int

## Helper functions


def new_session():
    session = Session()
    session.auth = HTTPBasicAuth(config.AUTH_USERNAME, config.AUTH_PASSWORD)
    return session


def retry(n: int):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            errors = []
            for _ in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    errors.append(e)
                    time.sleep(0.5)
            raise Exception(errors)

        return inner

    return decorator


## Main class


class DogeIndexerClient:
    def __init__(self) -> None:
        self._client = DogeClient()
        self.workers = [new_session() for _ in range(config.NUMBER_OF_WORKERS)]
        self.toplevel_worker = self.workers[0]

        # Determining starting block height for indexing
        self.latest_processed_block_height = self.extract_initial_block_height()

    def extract_initial_block_height(self) -> int:
        """
        Extracts the initial block height from the config
        """
        latest_block = DogeBlock.objects.order_by("block_number").last()
        if latest_block is None:
            return config.INITIAL_BLOCK_HEIGHT

        if latest_block.block_number < config.INITIAL_BLOCK_HEIGHT:
            raise Exception(
                f"Starting processing from block {config.INITIAL_BLOCK_HEIGHT}"
                f" with latest block in db: {latest_block.block_number} would"
                " create holes in the transaction history"
            )
        return latest_block.block_number

    def run(self) -> None:
        """
        Runs the indexing process in a endless loop
        """
        while True:
            height = self._get_current_block_height(self.toplevel_worker)
            if self.latest_processed_block_height < height - config.NUMBER_OF_BLOCK_CONFIRMATIONS:
                for i in range(
                    self.latest_processed_block_height + 1, height - config.NUMBER_OF_BLOCK_CONFIRMATIONS + 1
                ):
                    start = time.time()
                    self.process_block(i)
                    print(f"Processed block: {i} in: ", time.time() - start)
                    self.latest_processed_block_height = i
            else:
                print(f"No new blocks to process, sleeping for {config.INDEXER_POLL_INTERVAL} seconds")
                time.sleep(config.INDEXER_POLL_INTERVAL)

    ## Base methods for interacting with node directly

    @retry(5)
    def _get_current_block_height(self, worker: Session) -> int:
        return self._client.get_block_height(worker).json()["result"]

    @retry(5)
    def _get_block_hash_from_height(self, block_height: int, worker: Session) -> str:
        return self._client.get_block_hash_from_height(worker, block_height).json()["result"]

    # TODO: type hint (IBlockResponse)
    @retry(5)
    def _get_block_by_hash(self, block_hash: str, worker: Session) -> Any:
        return self._client.get_block_by_hash(worker, block_hash).json()["result"]

    # TODO: type hint (ITransactionResponse)
    @retry(5)
    def _get_transaction(self, txid: str, worker: Session) -> Any:
        return self._client.get_transaction(worker, txid).json()["result"]

    # Block processing part
    def process_block(self, block_height: int):
        # TODO: we always assume that block processing is for blocks that are for sure on main branch of the blockchain

        processed_blocks: BlockProcessorMemory = {"tx": [], "vins": [], "vins_cb": [], "vouts": []}
        process_queue: queue.Queue = queue.Queue()

        block_hash = self._get_block_hash_from_height(block_height, self.toplevel_worker)
        res_block = self._get_block_by_hash(block_hash, self.toplevel_worker)

        tx_ids = res_block["tx"]
        block_info: BlockInformationPassing = {
            "block_num": res_block["height"],
            "block_ts": res_block["time"],
        }

        block_db = DogeBlock.object_from_node_response(res_block)

        # Put all of the transaction in block on the processing queue
        for tx in tx_ids:
            process_queue.put(process_toplevel_transaction(process_queue, tx, block_info, self._get_transaction))

        # multithreading part of the processing
        workers = []
        for worker_index in range(config.NUMBER_OF_WORKERS):
            t = threading.Thread(
                target=thread_worker, args=(self.workers[worker_index], process_queue, processed_blocks)
            )
            workers.append(t)
            t.start()

        [t.join() for t in workers]

        # TODO: think about handling this in 2 steps of multithreading

        # Save to DB (this can be done in parallel) with other block processing
        with transaction.atomic():
            DogeTransaction.objects.bulk_create(processed_blocks["tx"], batch_size=999)
            TransactionInputCoinbase.objects.bulk_create(processed_blocks["vins_cb"], batch_size=999)
            TransactionInput.objects.bulk_create(processed_blocks["vins"], batch_size=999)
            TransactionOutput.objects.bulk_create(processed_blocks["vouts"], batch_size=999)
            DogeBlock.objects.bulk_create([block_db])


## Block processing functions


def process_toplevel_transaction(
    process_queue: queue.Queue,
    txid: str,
    block_info: BlockInformationPassing,
    transaction_getter: Callable,
):
    """Return the function that processes each individual transaction and fills the processing queue with all necessary additional tasks this creates

    Args:
        process_queue (queue.Queue): a queue that is shared between all workers and contains all the tasks that need to be processed
        txid (str): transaction id to process
        block_num (int): information about block number this transaction is a part of
        block_ts (int): information about block timestamp this transaction is a part of
    """

    def _process_toplevel_transaction(session: Session, processed_block: BlockProcessorMemory):
        res = transaction_getter(txid, session)

        tx_link = DogeTransaction.object_from_node_response(res, block_info["block_num"], block_info["block_ts"])
        processed_block["tx"].append(tx_link)

        for ind, vin in enumerate(res["vin"]):
            process_queue.put(process_pre_vout_transaction(vin, ind, tx_link.transaction_id, transaction_getter))

        for vout in res["vout"]:
            processed_block["vouts"].append(TransactionOutput.object_from_node_response(vout, tx_link.transaction_id))

        return True

    return _process_toplevel_transaction


def process_pre_vout_transaction(
    vin: IUtxoVinTransaction,
    vin_n: int,
    tx_link: str,
    transaction_getter: Callable,
):
    """Return the function that processes the transaction prevouts and link it to the spending transaction

    Args:
        vin (IUtxoVinTransaction): vin object from spending transaction
        vin_n (int): index of vin in spending transaction
        tx_link (str): transaction id of spending transaction
    """

    def _process_pre_vout_transaction(session: Session, processed_block: BlockProcessorMemory):
        if "txid" not in vin or "vout" not in vin:
            # Only coinbase transactions have no txid
            processed_block["vins_cb"].append(TransactionInputCoinbase.object_from_node_response(vin_n, vin, tx_link))
            return True
        txid, vout_n = vin["txid"], vin["vout"]
        res = transaction_getter(txid, session)
        prevout_res = res["vout"][vout_n]
        processed_block["vins"].append(TransactionInput.object_from_node_response(vin_n, vin, prevout_res, tx_link))
        return True

    return _process_pre_vout_transaction


def thread_worker(session: Session, process_queue: queue.Queue, processed_block: BlockProcessorMemory):
    while not process_queue.empty():
        item = process_queue.get()
        if callable(item):
            item(session, processed_block)
        break
