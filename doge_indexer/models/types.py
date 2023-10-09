from typing import List, TypedDict


# Transaction node response
class IUtxoScriptSig(TypedDict):
    asm: str
    hex: str


class __utxoScriptPubKeyBase(TypedDict, total=False):
    reqSigs: str
    addresses: List[str]
    address: str


class IUtxoScriptPubKey(__utxoScriptPubKeyBase):
    asm: str
    hex: str
    type: str  # choices :  "witness_v0_keyhash",


class IUtxoVoutTransaction(TypedDict):
    value: int
    n: int
    scriptPubKey: IUtxoScriptPubKey


class __UtxoVinTransactionBase(TypedDict, total=False):
    coinbase: str
    txid: str
    vout: int
    scriptSig: IUtxoScriptSig
    txinwitness: List[str]


class IUtxoVinTransaction(__UtxoVinTransactionBase):
    sequence: int


class IUtxoVinTransactionExtended(IUtxoVinTransaction):
    """
    Note that this type of response is only available for BTC, we want to be able to return this on DOGE indexer to be in line with BTC implementation
    """

    prevout: IUtxoVoutTransaction


class ITransactionResponse(TypedDict):
    txid: str
    hash: str
    version: int
    size: int
    vsize: int
    weight: int
    locktime: int
    vin: List[IUtxoVinTransaction]
    vout: List[IUtxoVoutTransaction]
    hex: str
    blockhash: str
    confirmations: int
    time: int
    blocktime: int


# Block node response
# TODO:


class IBlockResponse(TypedDict):
    size: int
    strippedsize: int
    weight: int
    nTx: int
    tx: List[str]
    hash: str
    confirmations: int
    height: int
    version: int
    versionHex: str
    merkleroot: str
    time: int
    mediantime: int
    nonce: int
    bits: str
    difficulty: int
    chainwork: str
    nTx: int
    previousblockhash: str
    nextblockhash: str
