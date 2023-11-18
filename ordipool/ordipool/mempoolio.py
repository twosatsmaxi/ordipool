import sys
from multiprocessing.pool import ThreadPool

import requests

from ordipool.models.transaction_info import MempoolTransactionInfo, TransactionVinVoutItem
from ordipool.utils.utils import extract_ordinal_content_from_tx


class Mempool:
    base_url = "https://mempool.space/api"
    thread_pool = ThreadPool(processes=50)

    def __init__(self, base_url="https://mempool.space/api", thread_pool_size=50):
        self.base_url = base_url
        self.thread_pool = ThreadPool(processes=thread_pool_size)

    def get_transaction_info(self, tx_id):
        url = self.base_url + "/tx/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        effectie_fee_rate = self.get_effective_fee_rate(tx_id)
        return MempoolTransactionInfo(
            effective_fee_rate=effectie_fee_rate,
            confirmed=json["status"]["confirmed"],
            fee=json["fee"],
            weight=json["weight"],
            block_height=json["status"]["block_height"] if "block_height" in json["status"] else sys.maxsize,
        )

    def get_effective_fee_rate(self, tx_id) -> int:
        url = self.base_url + "/v1/cpfp/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        return int(json["effectiveFeePerVsize"]) if "effectiveFeePerVsize" in json else None

    # get net spent for address on transaction in sats
    def get_net_spent_for_address_on_transaction(self, address: str, tx_id: str) -> int:
        url = self.base_url + "/tx/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        net_spent = 0
        for vin in json["vin"]:
            if vin["prevout"]["scriptpubkey_address"] == address:
                net_spent += vin["prevout"]["value"]
        for output in json["vout"]:
            if "scriptpubkey_address" in output and output["scriptpubkey_address"] == address:
                net_spent -= output["value"]
        # deduct fee
        # net_spent -= json["fee"]
        return net_spent

    def get_inscription_content_from_transaction(self, tx_id):
        url = self.base_url + "/tx/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        return extract_ordinal_content_from_tx(json)

    def get_vin_addresses(self, tx_id):
        url = self.base_url + "/tx/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        vin_addresses = set()
        for vin in json["vin"]:
            if "prevout" in vin and "scriptpubkey_address" in vin["prevout"]:
                vin_addresses.add(vin["prevout"]["scriptpubkey_address"])
        return vin_addresses

    def get_vout_transaction_item(self, tx_id) -> list[TransactionVinVoutItem]:
        url = self.base_url + "/tx/" + tx_id
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        vout_transaction_items = list()
        for vout in json["vout"]:
            if "scriptpubkey_address" in vout:
                transaction_vin_vout_item = TransactionVinVoutItem(address=vout["scriptpubkey_address"],
                                                                   value=vout["value"])
                vout_transaction_items.append(transaction_vin_vout_item)
        return vout_transaction_items

    def get_mempool_block_hash_by_block_number(self, block_number):
        url = self.base_url + "/block-height/" + str(block_number)
        res = requests.get(url)
        if res.status_code == 200:
            block_hash = res.text
        else:
            raise Exception("Error getting block info")
        return block_hash

    def get_mempool_transaction_ids(self, block_number):
        hash = self.get_mempool_block_hash_by_block_number(block_number)
        url = self.base_url + "/block/" + hash + "/txids"
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting block info")
        return json

    def get_mempool_transactions(self, block_number):
        hash = self.get_mempool_block_hash_by_block_number(block_number)
        url = self.base_url + "/block/" + hash + "/txs"
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting block info")
        return json

    def get_mempool_block_bulk_basic_from_start(self, start):
        url = self.base_url + "/blocks/" + str(start)
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting block info")
        return json

    def get_mempool_bulk(self, from_block: int, to_block: int) -> list[object]:
        # create a list of numbes from from_block to to_block
        # and chunk it into 10
        # then get the mempool transactions for each block
        # and return a list of transactions
        ranges = range(to_block, from_block, -15)
        block_details = self.thread_pool.map(self.get_mempool_block_bulk_basic_from_start, ranges)
        blocks = []
        for block in block_details:
            blocks.extend(block)
        return blocks

    def get_all_tx_value_in_block(self, block_number):
        txs = self.get_mempool_transactions(block_number)
        # take sum of all vout value in each transaction
        tx_out_values = []
        for tx in txs:
            tx_out_values.append(sum([vout["value"] for vout in tx["vout"]]))
        return tx_out_values

    def get_all_mempool_transactions_for_an_address(self, address):
        url = self.base_url + "/address/" + address + "/txs/mempool"
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting address info")
        return json

    def get_rbf_for_transaction(self, tx_id):
        url = self.base_url + "/v1/tx/" + tx_id+"/rbf"
        res = requests.get(url)
        if res.status_code == 200:
            json = res.json()
        else:
            raise Exception("Error getting transaction info")
        return json

