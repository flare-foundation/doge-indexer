from django.contrib import admin

from doge_indexer.models import DogeBlock, DogeTransaction, TransactionInput, TransactionOutput, TransactionInputCoinbase

class TransactionInputInline(admin.TabularInline):
    model = TransactionInput
    extra = 0
    fields = ("vin_n", "value", "script_key_address", "n", "vin_vout_index" ,"vin_previous_txid")
    readonly_fields = fields

class TransactionInputCoinbaseInline(admin.TabularInline):
    model = TransactionInputCoinbase
    extra = 0
    fields = ("vin_n", "vin_coinbase", "script_key_address", "n", "vin_previous_txid")
    readonly_fields = fields

class TransactionOutputInline(admin.TabularInline):
    model = TransactionOutput
    extra = 0
    readonly_fields = ("n", "value", "script_key_address")


@admin.register(DogeTransaction)
class DogeTransactionAdmin(admin.ModelAdmin):
    list_display = ("transactionId", "blockNumber", "timestamp", "paymentReference")
    search_fields = ("transactionId", "blockNumber")
    ordering = ("-timestamp",)

    inlines = [TransactionInputInline, TransactionOutputInline]
    