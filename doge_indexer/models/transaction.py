from django.db import models

from doge_indexer.models.model_utils import HexString32ByteField
from doge_indexer.models.types import ITransactionResponse
from doge_indexer.utils import is_valid_bytes_32_hex

ZERO_MIC = "0000000000000000000000000000000000000000000000000000000000000000"


class DogeTransaction(models.Model):
    transaction_id = HexString32ByteField(primary_key=True, db_column="transactionId")

    block_number = models.PositiveIntegerField(db_column="blockNumber")
    timestamp = models.PositiveBigIntegerField(db_column="timestamp")

    payment_reference = HexString32ByteField(db_column="paymentReference")

    # All transactions but coinbase are native payment transactions
    is_native_payment = models.BooleanField(default=False, db_column="isNativePayment")

    # TODO: update to enum field
    transaction_type = models.CharField(db_column="transactionType")

    # response = models.BinaryField(db_column="response")

    class Meta:
        indexes = (
            models.Index(fields=["block_number"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["payment_reference"]),
            models.Index(fields=["transaction_type"]),
        )

    def __str__(self) -> str:
        return f"Transaction {self.transaction_id} in block : {self.block_number}"

    @classmethod
    def object_from_node_response(cls, response: ITransactionResponse, block_number: int, timestamp: int):
        ref = cls.__extract_payment_reference(response)
        return cls(
            block_number=block_number,
            timestamp=timestamp,
            transaction_id=response["txid"],
            payment_reference=ref,
            is_native_payment=True,
            transaction_type="full_payment",
        )

    @staticmethod
    def __extract_payment_reference(response: ITransactionResponse):
        def is_op_return(vout):
            return (
                "scriptPubKey" in vout
                and "asm" in vout["scriptPubKey"]
                and vout["scriptPubKey"]["asm"].startswith("OP_RETURN")
            )

        std_references = []

        for vout in response["vout"]:
            if is_op_return(vout):
                # TODO: make it more bullet proof
                reference = vout["scriptPubKey"]["asm"].split(" ")[1]
                if is_valid_bytes_32_hex(reference):
                    std_references.append(reference)

        if len(std_references) == 1:
            return std_references[0]
        return ZERO_MIC
