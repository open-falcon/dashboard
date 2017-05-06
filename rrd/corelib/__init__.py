#-*- coding:utf-8 -*-
import requests
import json

def auth_requests(method, *args, **kwargs):
    from flask import g
    if not g.user_token:
        raise Exception("no api token")

    headers = {
        "Apitoken": json.dumps({"name":g.user_token.name, "sig":g.user_token.sig})
    }

    if not kwargs:
        kwargs = {}

    if "headers" in kwargs:
        headers.update(kwargs["headers"])
        del kwargs["headers"]

    if method == "POST":
        return requests.post(*args, headers=headers, **kwargs)
    elif method == "GET":
        return requests.get(*args, headers=headers, **kwargs)
    elif method == "PUT":
        return requests.put(*args, headers=headers, **kwargs)
    elif method == "DELETE":
        return requests.delete(*args, headers=headers, **kwargs)
    else:
        raise Exception("invalid http method")

