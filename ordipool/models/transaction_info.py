import dataclasses
import enum
from dataclasses import dataclass


@dataclass
class TransactionVinVoutItem:
    address: str
    value: int


@dataclass
class TransactionVin:
    tx_id: str
    prev_out: TransactionVinVoutItem

@dataclass
class MempoolTransactionInfo:
    confirmed: bool
    fee: int
    weight: int
    block_height: int
    effective_fee_rate: int = None

    def get_fee_rate(self) -> int:
        if self.effective_fee_rate is not None:
            return self.effective_fee_rate
        fee_rate = self.fee * 4 / self.weight
        # convert it to sats per byte and round it to the nearest integer
        return round(fee_rate)


@dataclass
class MempoolTransaction:
    tx_id: str
    effective_fee_rate: int
    confirmed: bool
    fee: int
    weight: int
    block_height: int
    vins: [TransactionVin]
    vouts: [TransactionVinVoutItem]

    def get_fee_rate(self) -> int:
        if self.effective_fee_rate is not None:
            return self.effective_fee_rate
        fee_rate = self.fee * 4 / self.weight
        # convert it to sats per byte and round it to the nearest integer
        return round(fee_rate)

