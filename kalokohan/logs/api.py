from django.http import HttpRequest
from ninja import Router, Schema

from kalokohan.logs.models import LogItem, LogItemSourceType, LogItemTypeType
from kalokohan.utils.security import AuthBearer

router = Router()


class LogItemSchema(Schema):
    type: LogItemTypeType
    source: LogItemSourceType
    message: str = ""


@router.post("/", auth=AuthBearer())
def log(
    request: HttpRequest,
    log_item: LogItemSchema,
) -> str:
    obj = LogItem.objects.create(
        type=log_item.type,
        source=log_item.source,
        message=log_item.message,
    )
    return str(obj.uuid)
