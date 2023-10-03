from django.db import models

from doge_indexer.models.model_utils import HexString32ByteField


class DogeBlock(models.Model):
    blockHash = HexString32ByteField(primary_key=True)

    blockNumber = models.PositiveIntegerField()
    timestamp = models.PositiveBigIntegerField()
    previousBlockHash = HexString32ByteField()

    # Number of transactions in block
    transactions = models.PositiveIntegerField()

    confirmed = models.BooleanField(default=False)

    # relevant only if confirmed not true
    numberOfConfirmations = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["blockNumber"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["previousBlockHash"]),
        ]

