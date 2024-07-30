import json
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
        name_placeholder.valid_params = valid_params

        return name_placeholder

    def create_post(self, method, api_endpoint, valid_params, valid_payload, func_name, docstring, accepts_header):
        def name_placeholder(self, **kwargs):
            return method(self, api_endpoint = api_endpoint, valid_params = valid_params, valid_payload = valid_payload, accepts_header = accepts_header,  **kwargs)

        name_placeholder.__doc__      = docstring
        name_placeholder.__name__     = func_name
        name_placeholder.api_endpoint = api_endpoint
        name_placeholder.valid_params = valid_params
        name_placeholder.valid_payload = valid_payload


        return name_placeholder

    def get_func(self, api_endpoint, valid_params, **kwargs):
        params = {k: v for k, v in kwargs.items() if k in valid_params and v is not None}

        api_endpoint = api_endpoint.format(**params)

        headers = self.header_base.copy()

        try:
            resp = req.get(
                url = self.API + api_endpoint,
                params = params,
                headers = headers
            )

            resp.raise_for_status()
            
        except Exception as e:
            print(f"HTTP error occurred: {e}")
            
        if resp.content:
            if "json" not in headers["accept"]:
                return resp.content

            else:
                return resp.json()

    def post_func(self, api_endpoint, valid_params, valid_payload, accepts_header, **kwargs):
        params  = {k: v for k, v in kwargs.items() if k in valid_params  and v is not None}
        payload = {k: v for k, v in kwargs.items() if k in valid_payload and v is not None}

        if "data" in payload.keys():
            payload = payload["data"]

        else:
            if len(valid_payload) == 1:
                payload = list(payload.values())[0]

            payload = json.dumps(payload)

        api_endpoint = api_endpoint.format(**params)

        headers = self.header_base.copy()
        headers["accept"] = accepts_header

        try:
            resp = req.post(
                url = self.API + api_endpoint,
                params  = params,
                data    = payload,
                headers = headers
            )

            resp.raise_for_status()

        except Exception as e:
            print(f"HTTP error occurred: {e}")

        if resp.content:
            if "json" not in headers["accept"]:
                return resp.content

            else:
                return resp.json()