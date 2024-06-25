import requests as req

class TorizonAPI():
    def __init__(self, token, API = "https://app.torizon.io/api/v2beta"):
        self.API    = API
        self.token  = token
        self.header_base = {
            "accept"        : "application/json",
            "Authorization" : f"Bearer {self.token}",
        }


    def create_func(self, method, api_endpoint, valid_params, func_name, docstring):
        def name_placeholder(self, **params):
            return method(self, api_endpoint = api_endpoint, valid_params = valid_params, **params)

        name_placeholder.__doc__  = docstring
        name_placeholder.__name__ = func_name
        
        return name_placeholder

    def get_func(self, api_endpoint, valid_params, **params):
        params = {k: v for k, v in params.items() if k in valid_params and v is not None}

        resp = req.get(
            url = self.API + api_endpoint,
            params = params,
            headers = self.header_base
        )

        return resp.json()