from django.db import models

from doge_indexer.models.model_utils import HexString32ByteField
from doge_indexer.models.types import (
    IUtxoScriptPubKey,
    IUtxoVinTransaction,
    IUtxoVinTransactionExtended,
    IUtxoVoutTransaction,
)


class AbstractTransactionOutput(models.Model):
    n = models.PositiveIntegerField()
    # currently total circulating supply fits in 20 digits
    value = models.DecimalField(max_digits=22, decimal_places=8)

    script_key_asm = models.CharField()
    script_key_hex = models.CharField()
    script_key_req_sigs = models.CharField(blank=True, null=True)
    script_key_type = models.CharField()
    script_key_address = models.CharField(max_length=64)

    class Meta:
        abstract = True
        indexes = (models.Index(fields=["script_key_address"]),)

    def to_vout_response(self) -> IUtxoVoutTransaction:
        print(self.value)
        script_pub_key: IUtxoScriptPubKey = {
            "asm": self.script_key_asm,
            "hex": self.script_key_hex,
            "type": self.script_key_type,
            "address": self.script_key_address,
        }
        if self.script_key_req_sigs:
            script_pub_key["reqSigs"] = self.script_key_req_sigs
        return {"value": 0, "n": self.n, "scriptPubKey": script_pub_key}


class TransactionOutput(AbstractTransactionOutput):
    transaction_link = models.ForeignKey("DogeTransaction", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("transaction_link", "n"),)

    @classmethod
    def object_from_node_response(cls, response: IUtxoVoutTransaction, transaction_link_id: str):
        script_pub_key = response["scriptPubKey"]
        if "address" in script_pub_key:
            address = script_pub_key["address"]
        if "addresses" in script_pub_key:
            address = script_pub_key["addresses"][0]
        else:
            address = ""
        return cls(
            transaction_link_id=transaction_link_id,
            n=response["n"],
            value=response["value"],
            script_key_asm=script_pub_key["asm"],
            script_key_hex=script_pub_key["hex"],
            script_key_req_sigs=script_pub_key.get("reqSigs"),
            script_key_type=script_pub_key["type"],
            script_key_address=address,
        )


class TransactionInputCoinbase(models.Model):
    transaction_link = models.ForeignKey("DogeTransaction", on_delete=models.CASCADE)

    # Position in vin array of transaction (always 0 for coinbase)
    vin_n = models.PositiveIntegerField()

    vin_coinbase = models.CharField()
    vin_sequence = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"Coinbase vin for tx: {self.transaction_link.transaction_id}"

    @classmethod
    def object_from_node_response(cls, vin_n: int, vin_response: IUtxoVinTransaction, transaction_link_id: str):
        assert vin_n == 0, "Coinbase transaction should always be first in vin array"
        if "coinbase" in vin_response:
            return cls(
                transaction_link_id=transaction_link_id,
                vin_n=vin_n,
                vin_coinbase=vin_response["coinbase"],
                vin_sequence=vin_response["sequence"],
            )
        else:
            raise Exception("Not a coinbase transaction")

    def to_vin_response(self) -> IUtxoVinTransaction:
        return {
            "coinbase": self.vin_coinbase,
            "sequence": self.vin_sequence,
        }


class TransactionInput(AbstractTransactionOutput):
    transaction_link = models.ForeignKey("DogeTransaction", on_delete=models.CASCADE)

    # Position in vin array of transaction
    vin_n = models.PositiveIntegerField()

    vin_previous_txid = HexString32ByteField()
    vin_vout_index = models.PositiveIntegerField()
    vin_sequence = models.PositiveBigIntegerField()

    vin_script_sig_asm = models.CharField()
    vin_script_sig_hex = models.CharField()

    # TODO: Add witness data to db if needed

    class Meta:
        unique_together = (("transaction_link", "vin_n"),)
        # TODO: n and vin_vout_index should be the same

    def to_vin_response(self) -> IUtxoVinTransactionExtended:
        prevout = self.to_vout_response()
        # TODO: other fields should be all defined for non-coinbase transactions
        assert self.vin_previous_txid is not None
        assert self.vin_vout_index is not None
        assert self.vin_script_sig_asm is not None
        assert self.vin_script_sig_hex is not None
        return {
            "txid": self.vin_previous_txid,
            "vout": self.vin_vout_index,
            "scriptSig": {
                "asm": self.vin_script_sig_asm,
                "hex": self.vin_script_sig_hex,
            },
            "sequence": self.vin_sequence,
            "prevout": prevout,
        }

    @classmethod
    def object_from_node_response(
        cls,
        vin_n: int,
        vin_response: IUtxoVinTransaction,
        vout_response: IUtxoVoutTransaction,
        transaction_link_id: str,
    ):
        vout_script_pub_key = vout_response["scriptPubKey"]
        if "address" in vout_script_pub_key:
            address = vout_script_pub_key["address"]
        if "addresses" in vout_script_pub_key:
            address = vout_script_pub_key["addresses"][0]
        else:
            address = ""

        if "coinbase" in vin_response:
            # TODO: create object TransactionInputCoinbase
            vin_response["coinbase"]
            original_txid = None
            vout_index = None
            script_sig_asm = None
            script_sig_hex = None
        else:
            assert "txid" in vin_response
            assert "vout" in vin_response
            assert "scriptSig" in vin_response
            original_txid = vin_response["txid"]
            vout_index = vin_response["vout"]
            script_sig_asm = vin_response["scriptSig"]["asm"]
            script_sig_hex = vin_response["scriptSig"]["hex"]

        return cls(
            transaction_link_id=transaction_link_id,
            vin_n=vin_n,
            # (pre)vout part
            n=vout_response["n"],
            value=vout_response["value"],
            script_key_asm=vout_script_pub_key["asm"],
            script_key_hex=vout_script_pub_key["hex"],
            script_key_req_sigs=vout_script_pub_key.get("reqSigs"),
            script_key_type=vout_script_pub_key["type"],
            script_key_address=address,
            # vin part
            vin_previous_txid=original_txid,
            vin_vout_index=vout_index,
            vin_sequence=vin_response["sequence"],
            vin_script_sig_asm=script_sig_asm,
            vin_script_sig_hex=script_sig_hex,
        )
