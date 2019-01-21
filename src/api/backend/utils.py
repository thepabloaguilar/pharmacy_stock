import os
import json
import requests

from flask import request
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


def request_to_myself(verb, route, params=None, data=None,
                      headers={}, add_token=True):
    if add_token:
        headers.update({'Token': request.headers.get('Token', '')})
    
    data = json.dumps(data) if data else data
    response = requests.request(
        verb,
        f'http://127.0.0.1:5000/api{route}',
        params=params,
        data=data,
        headers=headers)
    return response
