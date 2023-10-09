from rest_framework import serializers

from doge_indexer.models import DogeTransaction, TransactionInput, TransactionInputCoinbase, TransactionOutput


class TransactionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInput
        fields = "__all__"


class TransactionInputCoinbaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInputCoinbase
        fields = "__all__"


class TransactionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionOutput
        fields = "__all__"


class TransactionDetailSerializers(serializers.ModelSerializer):
    transactioninput_set = TransactionInputSerializer(many=True)
    transactioninputcoinbase_set = TransactionInputCoinbaseSerializer(many=True)
    transactionoutput_set = TransactionOutputSerializer(many=True)

    class Meta:
        model = DogeTransaction
        fields = "__all__"
