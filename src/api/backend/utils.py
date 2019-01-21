import os
import json

from datetime import date, datetime
from decimal import Decimal


def _json_encoder(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')


def _json_result(result):
    return json.loads(json.dumps(result, default=_json_encoder))
