from datetime import date

from dateutil.relativedelta import relativedelta

from .models import WeightItem
from .types import LbsKg, LbsKgDate


def lbs_to_kg(lbs: float) -> float:
    # 2 decimal places
    return round(lbs * 0.45359237, 2)


def get_current_weight() -> LbsKgDate:
    weight_item = WeightItem.objects.first()

    if weight_item is None:
        return LbsKgDate(lbs=0, kg=0, date=date(1970, 1, 1))

    return LbsKgDate(
        lbs=float(weight_item.weight_lbs),
        kg=lbs_to_kg(float(weight_item.weight_lbs)),
        date=weight_item.weighed_at,
    )


def get_max_weight() -> LbsKgDate:
    weight_item = WeightItem.objects.order_by("-weight_lbs").first()

    if weight_item is None:
        return LbsKgDate(lbs=0, kg=0, date=date(1970, 1, 1))

    return LbsKgDate(
        lbs=float(weight_item.weight_lbs),
        kg=lbs_to_kg(float(weight_item.weight_lbs)),
        date=weight_item.weighed_at,
    )


def get_past_12_months_delta() -> LbsKg:
    weight_items = WeightItem.objects.filter(
        weighed_at__gte=date.today() - relativedelta(months=12, day=1),
        weighed_at__lt=date.today(),
    )

    first = weight_items.first()
    last = weight_items.last()

    if first is None or last is None:
        return LbsKg(lbs=0, kg=0)

    diff_lbs = first.weight_lbs - last.weight_lbs

    return LbsKg(
        lbs=float(diff_lbs),
        kg=lbs_to_kg(float(diff_lbs)),
    )


def get_past_12_months_delta_by_month() -> list[LbsKgDate]:
    filter_kwargs_list = [
        {
            "weighed_at__gte": date.today() - relativedelta(months=i + 1, day=1),
            "weighed_at__lt": date.today() - relativedelta(months=i, day=1),
        }
        for i in range(10, -2, -1)
    ]

    deltas = []

    for filter_kwargs in filter_kwargs_list:
        end_date = filter_kwargs["weighed_at__lt"] - relativedelta(days=1)
        weight_items = WeightItem.objects.filter(**filter_kwargs)
        first = weight_items.first()
        last = weight_items.last()

        if first is None or last is None:
            deltas.append(LbsKgDate(lbs=0, kg=0, date=end_date))
            continue

        diff_lbs = first.weight_lbs - last.weight_lbs

        deltas.append(
            LbsKgDate(
                lbs=float(diff_lbs),
                kg=lbs_to_kg(float(diff_lbs)),
                date=end_date,
            )
        )

    return deltas
