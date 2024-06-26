import json
import yaml
import requests as req

class TorizonAPI():
    def __init__(self, token, API = "https://app.torizon.io/api/v2beta"):
        self.API    = API
        self.token  = token
        self.header_base = {
            "accept"        : "application/json",
            "Authorization" : f"Bearer {self.token}",
        }


    def create_get(self, method, api_endpoint, valid_params, func_name, docstring, accepts_header = "application/json"):
        def name_placeholder(self, **params):
            return method(self, api_endpoint = api_endpoint, valid_params = valid_params, **params)

        name_placeholder.__doc__  = docstring
        name_placeholder.__name__ = func_name
        name_placeholder.api_endpoint = api_endpoint

        return name_placeholder

    def create_post(self, method, api_endpoint, valid_params, valid_payload, func_name, docstring, accepts_header):
        def name_placeholder(self, **kwargs):
            return method(self, api_endpoint = api_endpoint, valid_params = valid_params, valid_payload = valid_payload, accepts_header = accepts_header,  **kwargs)

        name_placeholder.__doc__      = docstring
        name_placeholder.__name__     = func_name
        name_placeholder.api_endpoint = api_endpoint

        return name_placeholder

    def get_func(self, api_endpoint, valid_params, **kwargs):
        params = {k: v for k, v in kwargs.items() if k in valid_params and v is not None}

        api_endpoint = api_endpoint.format(**params)

        headers = self.header_base.copy()

        resp = req.get(
            url = self.API + api_endpoint,
            params = params,
            headers = headers
        )

        resp.raise_for_status()

        if resp.content:
            if "json" not in headers["accept"]:
                return resp.content

            else:
                return resp.json()

    def post_func(self, api_endpoint, valid_params, valid_payload, accepts_header, **kwargs):
        params  = {k: v for k, v in kwargs.items() if k in valid_params  and v is not None}
        payload = {k: v for k, v in kwargs.items() if k in valid_payload and v is not None}

        api_endpoint = api_endpoint.format(**params)

        headers = self.header_base.copy()
        headers["accept"] = accepts_header

        resp = req.post(
            url = self.API + api_endpoint,
            params  = params,
            data    = json.dumps(payload),
            headers = headers
        )

        resp.raise_for_status()

        if resp.content:
            if "json" not in headers["accept"]:
                return resp.content

            else:
                return resp.json()