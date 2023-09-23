from datetime import date
from typing import TypedDict


class LbsKg(TypedDict):
    lbs: float
    kg: float


class LbsKgDate(LbsKg):
    date: date
