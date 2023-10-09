from django.db import models

from doge_indexer.models.model_utils import HexString32ByteField
from doge_indexer.models.types import IBlockResponse


class DogeBlock(models.Model):
    block_hash = HexString32ByteField(primary_key=True)

    block_number = models.PositiveIntegerField()
    timestamp = models.PositiveBigIntegerField()
    previous_block_hash = HexString32ByteField()

    # Number of transactions in block
    transactions = models.PositiveIntegerField()

    confirmed = models.BooleanField(default=False)

    # relevant only if confirmed not true
    # TODO: GrePod why
    # number_of_confirmations = models.PositiveIntegerField()

    class Meta:
        indexes = (
            models.Index(fields=["block_number"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["previous_block_hash"]),
        )

    def __str__(self) -> str:
        return f"Block {self.block_number} : {self.block_hash}"

    @classmethod
    def object_from_node_response(cls, response: IBlockResponse):
        return cls(
            block_number=response["height"],
            timestamp=response["time"],
            block_hash=response["hash"],
            previous_block_hash=response["previousblockhash"],
            transactions=len(response["tx"]),
            confirmed=True,
        )
