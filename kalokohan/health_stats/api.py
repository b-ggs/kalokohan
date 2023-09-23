from datetime import date
from typing import TypedDict

from django.http.request import HttpRequest
from ninja import Router, Schema

from . import queries
from .models import WeightItem
from .security import SubmitWeightItemAuthBearer
from .types import LbsKg, LbsKgDate

router = Router()


class SummaryResponse(TypedDict):
    current_weight: LbsKgDate
    max_weight: LbsKgDate
    past_12_months_delta: LbsKg
    past_12_months_delta_by_month: list[LbsKgDate]


@router.get("/summary/", response=SummaryResponse)
def summary(request: HttpRequest) -> SummaryResponse:
    return SummaryResponse(
        current_weight=queries.get_current_weight(),
        max_weight=queries.get_max_weight(),
        past_12_months_delta=queries.get_past_12_months_delta(),
        past_12_months_delta_by_month=queries.get_past_12_months_delta_by_month(),
    )


class WeightItemSchema(Schema):
    weighed_at: date
    weight_lbs: float


@router.post("/submit-weight-item/", auth=SubmitWeightItemAuthBearer())
def submit_weight_item(
    request: HttpRequest,
    weight_item: WeightItemSchema,
) -> None:
    WeightItem.objects.update_or_create(
        weighed_at=weight_item.weighed_at,
        defaults={"weight_lbs": weight_item.weight_lbs},
    )
