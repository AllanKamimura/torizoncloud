from torizon_api import TorizonAPI

import requests as req
import yaml

class TorizonCloud():
    def __init__(self, openapi_yaml = "https://app.torizon.io/api/docs/torizon-openapi.yaml"):
        self.openapi_yaml = openapi_yaml

        self.data = self.load_yaml(self.openapi_yaml)

    def real_init(self):
        self.api           = TorizonAPI(self.token)
        self.endpoint_list = self.createEndpoints()

    def load_yaml(self, openapi_yaml):
        f = req.get(openapi_yaml).content
        raw_data = yaml.safe_load(f)

        data = self.resolve_refs(raw_data, raw_data)

        print(f'Welcome to {data["info"]["title"]} API version ({data["info"]["version"]})')

        return data

    def resolve_refs(self, data, root):
        if isinstance(data, dict):
            if '$ref' in data:
                ref_path = data['$ref'].split('/')[1:]  # Remove the initial '#/' and split the path
                ref_value = root
                for part in ref_path:
                    ref_value = ref_value[part]
                return self.resolve_refs(ref_value, root)  # Recursively resolve the reference
            else:
                return {key: self.resolve_refs(value, root) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.resolve_refs(item, root) for item in data]
        else:
            return data

    def login(self, client_id, client_secret):
        get_token_url = self.data["components"]["securitySchemes"]["Oauth2"]["flows"]["clientCredentials"]["tokenUrl"]

        # Form-encoded data
        payload = {
            "grant_type"   : "client_credentials",
            "client_id"    : client_id,
            "client_secret": client_secret
        }

        # Send POST request
        response = req.post(
            url = get_token_url,
            data = payload,
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            )

        response.raise_for_status()

        self.token = response.json()["access_token"]

        self.real_init()

    def createEndpoints(self):
        endpoint_list = []

        for endpoint_path in self.data["paths"].keys():
            endpoint = self.data["paths"][endpoint_path]

            if "get" in endpoint:
                endpoint_info = endpoint["get"]

                parameter_string = ""
                valid_parameters = []
                if "parameters" in endpoint_info.keys():
                    for parameter in endpoint_info["parameters"]:
                        valid_parameters.append(parameter["name"])

                        required = "required" if parameter["required"] else "optional"
                        schema = parameter["schema"].copy()
                        del schema["type"]

                        parameter_string += f'\t{parameter["name"]:<20} ({parameter["schema"]["type"]:<7}, {required:<8}): {schema}\n'

                docstring = f"""\n
{endpoint_info["description"]}
Parameters:
{parameter_string}
"""
                endpoint_function = endpoint_info["operationId"].replace("-", "_")
                # Assigning the dynamically created method to the class
                setattr(TorizonAPI,
                        endpoint_function,
                        TorizonAPI.create_func(
                            self.api,
                            method = TorizonAPI.get_func, 
                            api_endpoint = endpoint_path,
                            valid_params = valid_parameters,
                            func_name = endpoint_function, 
                            docstring = docstring))

                endpoint_list.append(endpoint_function)

            # if "post" in endpoint:
            #     endpoint_info = endpoint["post"]

        return endpoint_list