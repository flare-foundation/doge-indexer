from django.contrib import admin

from doge_indexer.models import (
    DogeBlock,
    DogeTransaction,
    TipSyncState,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)
from doge_indexer.models.sync_state import PruneSyncState


class TransactionInputInline(admin.TabularInline):
    model = TransactionInput
    extra = 0
    ordering = ("vin_n",)
    fields = ("vin_n", "value", "script_key_address", "n", "vin_vout_index", "vin_previous_txid")
    readonly_fields = fields


class TransactionInputCoinbaseInline(admin.TabularInline):
    model = TransactionInputCoinbase
    extra = 0
    ordering = ("vin_n",)
    fields = ("vin_n", "vin_coinbase")
    readonly_fields = fields


class TransactionOutputInline(admin.TabularInline):
    model = TransactionOutput
    extra = 0
    fields = ("n", "value", "script_key_address")
    readonly_fields = fields


@admin.register(DogeTransaction)
class DogeTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "block_number", "timestamp", "payment_reference")
    search_fields = ("transaction_id", "block_number")
    ordering = ("-timestamp",)

    inlines = (TransactionInputCoinbaseInline, TransactionInputInline, TransactionOutputInline)


@admin.register(DogeBlock)
class DogeBlockAdmin(admin.ModelAdmin):
    list_display = ("block_number", "timestamp", "block_hash", "transactions")
    search_fields = ("block_number", "block_hash")
    ordering = ("-timestamp",)


@admin.register(TipSyncState)
class TipSyncStateAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "sync_state", "latest_tip_height", "latest_indexed_height")
    fields = ("timestamp", "sync_state", "latest_tip_height", "latest_indexed_height")
    search_fields = ()


@admin.register(PruneSyncState)
class PruneSyncStateAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "latest_indexed_tail_height")
    fields = ("timestamp", "latest_indexed_tail_height")
    search_fields = ()
