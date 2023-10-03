from django.db import models

from doge_indexer.models.model_utils import HexString32ByteField
from doge_indexer.models.types import ITransactionResponse
from doge_indexer.utils import is_valid_bytes_32_hex

ZERO_MIC = '0000000000000000000000000000000000000000000000000000000000000000'

class DogeTransaction(models.Model):
    transactionId = HexString32ByteField(primary_key=True)

    blockNumber = models.PositiveIntegerField()
    timestamp = models.PositiveBigIntegerField()

    paymentReference = HexString32ByteField()

    # All transactions but coinbase are native payment transactions
    isNativePayment = models.BooleanField(default=False)

    transactionType = models.CharField()

    # response = models.BinaryField()

    class Meta:
        indexes = [
            models.Index(fields=["blockNumber"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["paymentReference"]),
            models.Index(fields=["transactionType"]),
        ]

    @classmethod
    def object_from_node_response(cls, response: ITransactionResponse, block_number: int, timestamp: int):
        ref = cls.__extract_payment_reference(response)
        return cls(
            blockNumber=block_number,
            timestamp=timestamp,
            transactionId=response["txid"],
            paymentReference=ref,
            isNativePayment=True,
            transactionType="full_payment",
        )


    # @classmethod
    # def create_from_node_response(cls, response: ITransactionResponse, block_number: int, timestamp: int):
    #     ref = cls.__extract_payment_reference(response)
    #     return cls.objects.create(
    #         blockNumber=block_number,
    #         timestamp=timestamp,
    #         transactionId=response["txid"],
    #         paymentReference=ref,
    #         isNativePayment=True,
    #         transactionType="full_payment",
    #     )

    @staticmethod
    def __extract_payment_reference(response: ITransactionResponse):
        def is_op_return(vout):
            return "scriptPubKey" in vout and "asm" in vout["scriptPubKey"] and vout["scriptPubKey"]["asm"].startswith("OP_RETURN")                                     

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
    

