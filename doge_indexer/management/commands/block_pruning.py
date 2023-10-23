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


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            time.sleep(config.PRUNE_INTERVAL_SECONDS)

            if not config.PRUNE_KEEP_DAYS:
                return

            now_ts = int(time.time())

            cutoff = now_ts - config.PRUNE_KEEP_DAYS * 24 * 60 * 60

            with transaction.atomic():
                # objects with fk to transaction first
                TransactionInput.objects.filter(transaction_link__timestamp__lt=cutoff).delete()
                TransactionInputCoinbase.objects.filter(transaction_link__timestamp__lt=cutoff).delete()
                TransactionOutput.objects.filter(transaction_link__timestamp__lt=cutoff).delete()

                # then others
                DogeBlock.objects.filter(timestamp__lt=cutoff).delete()
                DogeTransaction.objects.filter(timestamp__lt=cutoff).delete()
