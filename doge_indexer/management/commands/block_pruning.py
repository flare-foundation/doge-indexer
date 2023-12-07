import logging
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from configuration.config import config
from doge_indexer.models import (
    DogeBlock,
    DogeTransaction,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)
from doge_indexer.models.sync_state import PruneSyncState

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        prune_state = PruneSyncState.instance()
        while True:
            if not config.PRUNE_KEEP_DAYS:
                return

            now_ts = int(time.time())

            cutoff = now_ts - config.PRUNE_KEEP_DAYS * 24 * 60 * 60

            logger.info("Pruning at: %s", now_ts, " all transactions and block before cutoff: %s", cutoff)

            with transaction.atomic():
                # objects with fk to transaction first
                TransactionInput.objects.filter(transaction_link__timestamp__lt=cutoff).delete()
                TransactionInputCoinbase.objects.filter(transaction_link__timestamp__lt=cutoff).delete()
                TransactionOutput.objects.filter(transaction_link__timestamp__lt=cutoff).delete()

                # then others
                DogeBlock.objects.filter(timestamp__lt=cutoff).delete()
                DogeTransaction.objects.filter(timestamp__lt=cutoff).delete()

                bottom_block = DogeBlock.objects.order_by("block_number").first()
                bottom_block_transaction = DogeTransaction.objects.order_by("block_number").first()

                if bottom_block is not None and bottom_block_transaction is not None:
                    if bottom_block.block_number != bottom_block_transaction.block_number:
                        raise Exception("Bottom block and bottom transaction block number mismatch while pruning")

                    prune_state.latest_indexed_tail_height = bottom_block.block_number
                    prune_state.timestamp = now_ts
                    prune_state.save()

            logger.info("Sleeping for %s sec", config.PRUNE_INTERVAL_SECONDS)

            time.sleep(config.PRUNE_INTERVAL_SECONDS)
