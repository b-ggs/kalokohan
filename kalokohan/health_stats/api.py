from datetime import date

from django.http.request import HttpRequest
from ninja import Router, Schema

from .models import WeightItem
from .security import SubmitWeightItemAuthBearer

router = Router()


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
