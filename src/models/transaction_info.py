import dataclasses
import enum
from dataclasses import dataclass


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
class TransactionVinVoutItem:
    address: str
    value: int
