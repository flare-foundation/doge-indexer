from requests.auth import HTTPBasicAuth
from django.core.management.base import BaseCommand
from django.db import transaction


from doge_client.main import ClientInitConfig, DogeClient

import queue
from requests.sessions import Session
import threading

from pprint import pprint as pp
import time

from doge_indexer.models import DogeTransaction, TransactionInputCoinbase, TransactionInput, TransactionOutput
from doge_indexer.models.types import IUtxoVinTransaction

client_config: ClientInitConfig = {
    "url": "http://213.32.6.191:22555/",
    "username": "admin",
    "password": "b4987b3064d68a099d00d339fe72af92a09fa30b10306999be383d93c68ebfd5",
}

NUMBER_OF_WORKERS = 10


def process_blocks(from_block: int, to_block: int | None):
    pass


def process_block(workers, block_hash: str):
    start = time.time()
    client = DogeClient(client_config)
    ses0 = workers[0]

    process_queue = queue.Queue()

    # print("H: 000")

    res_block = client.get_block_by_hash(ses0, block_hash).json()
    tx_ids = res_block["result"]["tx"]
    block_num = res_block["result"]["height"]
    block_ts = res_block["result"]["time"]

    # print("H: 001")

    for tx in tx_ids:
        process_queue.put(process_toplevel_transaction(client, process_queue, tx, block_num, block_ts))

    print("len of p queue: ", process_queue.qsize())

    sessions = [new_session(client_config) for _ in range(NUMBER_OF_WORKERS)]
    workers = []
    processed_blocks = [{"tx": list(), "vins": list(), "vouts": list()} for _ in range(NUMBER_OF_WORKERS)]


    for worker_index in range(NUMBER_OF_WORKERS):
        t = threading.Thread(target=thread_worker, args=(sessions[worker_index], process_queue ,processed_blocks[worker_index]))
        workers.append(t)
        t.start()

    [t.join() for t in workers]

    # Start workers that empties both queues
    # while not top_level_tx_queue.empty():
    #     item = top_level_tx_queue.get()
    #     # print(item, item is None)
    #     if item is None:
    #         break
    #     item(ses0, processed_block)
    #     # print(top_level_tx_queue.qsize())

    # while not prevout_tx_queue.empty():
    #     item = prevout_tx_queue.get()
    #     if item is None:
    #         break
    #     item(ses0, processed_block)
    #     # print(prevout_tx_queue.qsize())
    
    print("In time 1: ", time.time() - start)
    # pp(processed_block)

    tot1, tot2, tot3 = 0, 0, 0

    for processed_block in processed_blocks:
        # pp(processed_block)
        tot1 += len(processed_block["tx"])
        tot2 += len(processed_block["vins"])
        tot3 += len(processed_block["vouts"])
        print("Tx len: ",len(processed_block["tx"]))
        print("Vin len: ",len(processed_block["vins"]))
        print("Vout len: ",len(processed_block["vouts"]))
        print(""" 
              ########################################################################################################################################################################################################################################################################
""")
              
    print("Total TX count: ", tot1)
    print("Total Vins count: ", tot2)
    print("Total Vouts count: ", tot3)
    # pp(processed_blocks)

    print("In time 2: ", time.time() - start)

    with transaction.atomic():
        for pr in processed_blocks:
            for tx in pr["tx"]:
                tx.save()
            for output in pr["vouts"]:
                output.save()
            for inp in pr["vins"]:
                inp.save()

    print("In time 3: ", time.time() - start)


def process_toplevel_transaction(client: DogeClient, process_queue: queue.Queue, txid: str, block_num: int, block_ts: int):
    """
    Return the function that processes the transaction

    Args:
        txid (str): transaction id
    """

    def _process_toplevel_transaction(session: Session, processed_block: dict):
        res = client.get_transaction(session, txid).json()
        # TODO: create object for db

        tx_link = DogeTransaction.object_from_node_response(res["result"], block_num, block_ts)
        processed_block["tx"].append(tx_link)

        for ind, vin in enumerate(res["result"]["vin"]):
            process_queue.put(process_pre_vout_transaction(client, vin, ind, tx_link))
        
        for vout in res["result"]["vout"]:
            processed_block["vouts"].append(
                TransactionOutput.object_from_node_response(vout, tx_link)
            )

        return True

    return _process_toplevel_transaction

# TODO: passing doge transaction as reference is not a good idea 
def process_pre_vout_transaction(client: DogeClient, vin: IUtxoVinTransaction, vin_n: int, tx_link: DogeTransaction):
    """
    Return the function that processes the transaction prevouts (vins vouts)

    Args:
        txid (str): transaction id
    """

    def _process_pre_vout_transaction(session: Session, processed_block: dict):
        if "txid" not in vin or "vout" not in vin:
            # Only coinbase transactions have no txid
            processed_block["vins"].append(
                TransactionInputCoinbase.object_from_node_response(vin_n, vin, tx_link)
            )
            return True
        txid, vout_n = vin["txid"], vin["vout"]
        res = client.get_transaction(session, vin["txid"]).json()
        prevout_res = res["result"]["vout"][vout_n]
        processed_block["vins"].append(
            TransactionInput.object_from_node_response(vin_n, vin, prevout_res, tx_link)
        )
        return True

    return _process_pre_vout_transaction

def thread_worker(session: Session, process_queue: queue.Queue, processed_block: dict):
    while not process_queue.empty():
        item = process_queue.get()
        if item is None:
            break
        item(session, processed_block)

def new_session(config: ClientInitConfig):
    session = Session()
    session.auth = HTTPBasicAuth(client_config["username"], client_config["password"])
    return session


blocks = [
    "6f1456dc45b7d42bd84234844769e15616c6f68e698f74e41a8ced40e258563e", # 823 tx,
    "25af14c0f0d4bc7da615c0c312da2cbfe9e512c38652c4d8beca675852ec9f7d", # semi new 
    "37bc436b81b813d84c2cab54c7f1b8fbd162942f49c14df0b4afe462cd2ce0bd", # 9 tx 10inputs 16 outputs 
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        workers = [new_session(client_config) for _ in range(NUMBER_OF_WORKERS)]

        process_block(workers, "37bc436b81b813d84c2cab54c7f1b8fbd162942f49c14df0b4afe462cd2ce0bd")
        # process_blocks(1, 2)
