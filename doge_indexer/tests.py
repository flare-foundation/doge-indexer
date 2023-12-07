from typing import Any

from django.test import TestCase

from doge_indexer.indexer import DogeIndexerClient
from doge_indexer.models import (
    DogeBlock,
    DogeTransaction,
    TransactionInput,
    TransactionInputCoinbase,
    TransactionOutput,
)
from doge_indexer.models.transaction import ZERO_REFERENCE

# Note that all of the tests are using the DOGE mainnet blockchain.
# See the .env.example file for the configuration.
# NODE_RPC_URL=url
# AUTH_USERNAME=user
# AUTH_PASSWORD=password
# To run the tests, you need to have a running PostgreSQL database.
# You can use the docker-compose.yml file to run the database.
# To run the tests, run the following command:
# manage.py test
# or
# coverage run manage.py test


class IndexingBlockWorkingTest(TestCase):
    def setUp(self):
        self.indexer = DogeIndexerClient()

    def test_should_index_block(self):
        """Testing indexing for block 4855034"""
        self.indexer.process_block(4855034)

        block_count = DogeBlock.objects.count()
        self.assertEqual(block_count, 1)
        transaction_from_block = DogeBlock.objects.get(block_number=4855034).transactions
        transaction_count = DogeTransaction.objects.count()
        inputs_count = TransactionInput.objects.count()
        outputs_count = TransactionOutput.objects.count()
        coinbase_count = TransactionInputCoinbase.objects.count()

        # print("transaction_count: ", transaction_count)

        self.assertEqual(transaction_count, 34)
        self.assertEqual(transaction_from_block, transaction_count)

        self.assertEqual(inputs_count, 60)
        self.assertEqual(outputs_count, 74)
        self.assertEqual(coinbase_count, 1)


# class IndexingBlockPerformanceTest(TestCase):
#     """
#     Note that this test case is a slow one, it takes about 1 minute to run.
#     """

#     def setUp(self):
#         self.indexer = DogeIndexerClient()

#     def test_should_index_block(self):
#         """Testing indexing for block 4738722"""

#         self.indexer.process_block(4738722)

#         transaction_from_block = DogeBlock.objects.get(block_number=4738722).transactions
#         transaction_count = DogeTransaction.objects.count()
#         inputs_count = TransactionInput.objects.count()
#         outputs_count = TransactionOutput.objects.count()
#         coinbase_count = TransactionInputCoinbase.objects.count()

#         self.assertEqual(transaction_count, 4233)
#         self.assertEqual(transaction_from_block, transaction_count)

#         self.assertEqual(inputs_count, 4455)
#         self.assertEqual(outputs_count, 8514)
#         self.assertEqual(coinbase_count, 1)


class TransactionLogicTest(TestCase):
    def setUp(self, **kwargs: Any) -> Any:
        self.indexer = DogeIndexerClient()
        self.indexer.process_block(4994995)

    def test_should_index_block(self):
        """Testing indexing for block 4994995"""
        transaction_count = DogeTransaction.objects.count()
        inputs_count = TransactionInput.objects.count()
        outputs_count = TransactionOutput.objects.count()
        coinbase_count = TransactionInputCoinbase.objects.count()

        self.assertEqual(transaction_count, 127)
        self.assertEqual(inputs_count, 735)
        self.assertEqual(outputs_count, 293)
        self.assertEqual(coinbase_count, 1)

    def test_should_coinbase_transaction_fields(self):
        tx_id = "8cba14a73c5de6e995ca170d948c2a35a4c94ddb702d515119fde5b2a482a1e5"
        coinbase_tx = DogeTransaction.objects.get(transaction_id=tx_id)

        self.assertEqual(coinbase_tx.transaction_id, tx_id)
        self.assertEqual(coinbase_tx.block_number, 4994995)
        self.assertEqual(coinbase_tx.timestamp, 1701867879)
        self.assertEqual(coinbase_tx.payment_reference, ZERO_REFERENCE)
        self.assertEqual(coinbase_tx.is_native_payment, False)
        self.assertEqual(coinbase_tx.transaction_type, "coinbase")

    def test_should_coinbase_transaction_inputs_count(self):
        coinbase_tx = DogeTransaction.objects.get(
            transaction_id="8cba14a73c5de6e995ca170d948c2a35a4c94ddb702d515119fde5b2a482a1e5"
        )

        inputs = coinbase_tx.transactioninput_set.all()
        cb_inputs = coinbase_tx.transactioninputcoinbase_set.all()
        outputs = coinbase_tx.transactionoutput_set.all()

        self.assertEqual(len(inputs), 0)
        self.assertEqual(len(cb_inputs), 1)
        self.assertEqual(len(outputs), 1)

    def test_should_coinbase_transaction_inputs_details(self):
        tx_id = "8cba14a73c5de6e995ca170d948c2a35a4c94ddb702d515119fde5b2a482a1e5"
        coinbase_tx = DogeTransaction.objects.get(transaction_id=tx_id)

        cb_inputs_set = coinbase_tx.transactioninputcoinbase_set.all()
        outputs_set = coinbase_tx.transactionoutput_set.all()

        coinbase = cb_inputs_set.first()
        output = outputs_set.first()

        assert coinbase is not None
        assert output is not None

        # Coinbase input part
        self.assertEqual(coinbase.transaction_link.transaction_id, tx_id)
        self.assertEqual(coinbase.vin_n, 0)
        self.assertEqual(coinbase.vin_coinbase, "03b3374c0101")
        self.assertEqual(coinbase.vin_sequence, 4294967295)

        # Coinbase output part
        self.assertEqual(output.transaction_link.transaction_id, tx_id)
        self.assertEqual(output.n, 0)
        self.assertEqual(output.value, "10024.42690947")
        self.assertEqual(output.script_key_address, "DTZSTXecLmSXpRGSfht4tAMyqra1wsL7xb")

    def test_should_full_payment_transaction_fields(self):
        tx_id = "e449018153f0792a3f8f10825594151dcb7a5e2ea302b542265353b8c48d337c"
        tx = DogeTransaction.objects.get(transaction_id=tx_id)

        self.assertEqual(tx.transaction_id, tx_id)
        self.assertEqual(tx.block_number, 4994995)
        self.assertEqual(tx.timestamp, 1701867879)
        self.assertEqual(tx.payment_reference, ZERO_REFERENCE)
        self.assertEqual(tx.is_native_payment, True)
        self.assertEqual(tx.transaction_type, "full_payment")

    def test_should_full_payment_transaction_inputs_count(self):
        tx_id = "e449018153f0792a3f8f10825594151dcb7a5e2ea302b542265353b8c48d337c"
        tx = DogeTransaction.objects.get(transaction_id=tx_id)

        inputs = tx.transactioninput_set.count()
        cb_inputs = tx.transactioninputcoinbase_set.count()
        outputs = tx.transactionoutput_set.count()

        self.assertEqual(inputs, 530)
        self.assertEqual(cb_inputs, 0)
        self.assertEqual(outputs, 2)

    def test_should_full_payment_transaction_outputs_details(self):
        tx_id = "e449018153f0792a3f8f10825594151dcb7a5e2ea302b542265353b8c48d337c"
        tx = DogeTransaction.objects.get(transaction_id=tx_id)

        outputs = tx.transactionoutput_set.all()

        output_0 = outputs.filter(n=0).first()
        assert output_0 is not None

        self.assertEqual(output_0.transaction_link.transaction_id, tx_id)
        self.assertEqual(output_0.n, 0)
        self.assertEqual(output_0.value, "20000.00000000")
        self.assertEqual(output_0.script_key_address, "DCrV1EMHh55feYvVCwHWy11rF1eypfMH4S")

        output_1 = outputs.filter(n=1).first()
        assert output_1 is not None

        self.assertEqual(output_1.transaction_link.transaction_id, tx_id)
        self.assertEqual(output_1.n, 1)
        self.assertEqual(output_1.value, "1.97615000")
        self.assertEqual(output_1.script_key_address, "DRKWVU2Zs3aFHgYLBXX8e9d7uMyY1WtmV4")
