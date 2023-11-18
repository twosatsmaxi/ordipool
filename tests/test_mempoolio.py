from unittest import TestCase

from ordipool.models.transaction_info import TransactionVinVoutItem
from ordipool.ordipool.mempoolio import Mempool


class TestMempool(TestCase):
    mempool = Mempool()

    def test_get_transaction_info(self):
        tx_id = "371ca437bb58169971fa7e9dbbb7aac6e961835c9b06dfcc01dead3586a94e21"
        mempool_transaction_info = self.mempool.get_transaction_info(tx_id)
        self.assertEqual(mempool_transaction_info.confirmed, True)
        self.assertEqual(mempool_transaction_info.fee, 1180)
        self.assertEqual(mempool_transaction_info.weight, 514)

    def test_get_net_spent_for_address_on_transaction(self):
        tx_id = "f09cc426a788c99f1eb6735838cc83579b7edd47e11b67aebbd6b6ba1eb25d24"
        address = "bc1ppq9v5r7cu7w9nc408jyucvtpl2wnnw7kcdfu425z0f0e35f4h5yswtykl3"
        net_spent = self.mempool.get_net_spent_for_address_on_transaction(address, tx_id)
        self.assertEqual(net_spent, -340006)

    def test_get_net_spent_for_address_on_transaction_for_another(self):
        tx_id = "ce34760684f38c06990be1c059d8fb382e7c473a37ae5f2b051efde8cd959258"
        address = "bc1p7zyy83sxtxy3n3e24tc9wwshzduj6g8z9x325l7kxd8gw4vs8qmqefum44"
        net_spent = self.mempool.get_net_spent_for_address_on_transaction(address, tx_id)
        self.assertEqual(net_spent, -546)

    def test_get_inscription_content_from_transaction(self):
        content = self.mempool.get_inscription_content_from_transaction(
            "a12ef285fc64b92b9920a5dc314366a3f8d9402fe9aacb8df45b6556ab0d8ec2")
        self.assertEqual(content, "808808.bitmap")

    def test_get_vin_addresses(self):
        tx_id = "0599e4ad4e54e5fd62c7440ff607c9026614822a77b40ebfa77f57122e299ba2"
        vin_addresses = self.mempool.get_vin_addresses(tx_id)
        self.assertEqual(vin_addresses, {"3LyhPP5ZEyikVga1r3LNvXmjRYT43bG7ZF",
                                         "bc1p5s8wkfdz5lwq3vef0nw7hd73qle99vzck99ju5x3u7pugl2wpyrs8tw3xd"})

    def test_get_vout_addresses(self):
        tx_id = "0599e4ad4e54e5fd62c7440ff607c9026614822a77b40ebfa77f57122e299ba2"
        vout_addresses = self.mempool.get_vout_transaction_item(tx_id)
        expected = [TransactionVinVoutItem(address='3LyhPP5ZEyikVga1r3LNvXmjRYT43bG7ZF',
                                           value=1800),
                    TransactionVinVoutItem(address='bc1psup82w0sfnc3v3jdfc03pljqpd0ede94y4f0q943m5cxuw8s3caqfasrhj',
                                           value=10000),
                    TransactionVinVoutItem(address='3Mj42CWbQAmcYpt7m6cEutuALCxqAuNC6S',
                                           value=1990370),
                    TransactionVinVoutItem(address='bc1qcq2uv5nk6hec6kvag3wyevp6574qmsm9scjxc2',
                                           value=50000),
                    TransactionVinVoutItem(address='3LyhPP5ZEyikVga1r3LNvXmjRYT43bG7ZF',
                                           value=600),
                    TransactionVinVoutItem(address='3LyhPP5ZEyikVga1r3LNvXmjRYT43bG7ZF',
                                           value=600),
                    TransactionVinVoutItem(address='3LyhPP5ZEyikVga1r3LNvXmjRYT43bG7ZF',
                                           value=240969)]
        self.assertEqual(vout_addresses, expected)

    def test_get_mempool_block_hash_by_block_number(self):
        block_height = 73555
        block_hash = self.mempool.get_mempool_block_hash_by_block_number(block_height)
        self.assertEqual(block_hash, "000000000028d82505359327e1370655831986ec73215bd5035007f571fe7a61")

    def test_get_mempool_transaction_ids(self):
        block_height = 73555
        transaction_ids = self.mempool.get_mempool_transaction_ids(block_height)
        self.assertEqual(transaction_ids, ['623c4f94810b996c6a5aa3b6bc3ae7a8ca58f56d35980bc0463ec33c89fe5bd8',
                                           '43bdb074c7608a2f426d62e1a3851c088d1f1169a40e42cc3886eb685582894c',
                                           '6a63298b705e9f53067e4c38834c55fb1d3aeb9b217406b159da14af204ec832',
                                           '74de0a80fd3fbfe732d3e59e66c630bddf5906345456d2fd8e345097bbd16269',
                                           'fef7f58ba7cd1f1d007e0f8f958ca9de77b3414197e1b5d3083420e3781f49ed'])

    def test_get_mempool_transactions(self):
        block_height = 73555
        transactions = self.mempool.get_mempool_transactions(block_height)
        # assert transactions size to be 5 exactly
        self.assertEqual(len(transactions), 5)

    def test_mempool_bulk(self):
        block_info = self.mempool.get_mempool_bulk(from_block=73550, to_block=73570)
        self.assertEqual(len(block_info), 20)

    def test_get_all_tx_size_in_block(self):
        block_height = 73555
        tx_size = self.mempool.get_all_tx_value_in_block(block_height)
        self.assertEqual(tx_size, [5000000000, 5000000000, 5000000000, 10000000000, 10000000000])

    def test_get_rbf_for_transaction(self):
        tx_id = '5718c479daefc71021ab684f796f329999acfdd1cb124ed2683733a891fd1534'
        rbf = self.mempool.get_rbf_for_transaction(tx_id)
        self.assertTrue(rbf['replacements'] is not None)

