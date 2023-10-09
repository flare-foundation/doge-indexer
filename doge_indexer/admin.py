from django.contrib import admin

from doge_indexer.models import (
    DogeTransaction,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)


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
    search_fields = ("transactionId", "block_number")
    ordering = ("-timestamp",)

    inlines = (TransactionInputCoinbaseInline, TransactionInputInline, TransactionOutputInline)
