import time
from django.db import transaction

from django.core.management.base import BaseCommand

from configuration.config import config
from doge_indexer.models import (
    DogeBlock,
    DogeTransaction,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)
from doge_indexer.models.sync_state import PruneSyncState


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            if not config.PRUNE_KEEP_DAYS:
                return

            now_ts = int(time.time())
            print(f"Pruning at: {now_ts}")

            cutoff = now_ts - config.PRUNE_KEEP_DAYS * 24 * 60 * 60

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

                    prune_state = PruneSyncState.get_the_one()
                    prune_state.latest_indexed_tail_height = bottom_block.block_number
                    prune_state.timestamp = now_ts
                    prune_state.save()

            print(f"Sleeping for {config.PRUNE_INTERVAL_SECONDS} sec")
            time.sleep(config.PRUNE_INTERVAL_SECONDS)
