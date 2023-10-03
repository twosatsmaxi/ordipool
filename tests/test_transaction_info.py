from unittest import TestCase

from ordipool.models.transaction_info import MempoolTransactionInfo


class TestMempoolTransactionInfo(TestCase):
    def test_get_fee_rate(self):
        mempool_transaction_info = MempoolTransactionInfo(confirmed=True, fee=1180, weight=514, block_height=1234)
        fee_rate = mempool_transaction_info.get_fee_rate()
        self.assertEqual(fee_rate, 9)

