from typing import TypedDict

from django.http import HttpRequest
from ninja import Router, Schema

from kalokohan.logs.models import LogItem, LogSourceType, LogTypeType
from kalokohan.utils.security import AuthBearer

router = Router()


class LogItemSchema(Schema):
    log_type: LogTypeType
    log_source: LogSourceType
    message: str = ""


class LogResponse(TypedDict):
    uuid: str


@router.post("/", auth=AuthBearer())
def log(
    request: HttpRequest,
    log_item: LogItemSchema,
) -> LogResponse:
    obj = LogItem.objects.create(
        log_type=log_item.log_type,
        log_source=log_item.log_source,
        message=log_item.message,
    )
    return LogResponse(
        uuid=str(obj.uuid),
    )
