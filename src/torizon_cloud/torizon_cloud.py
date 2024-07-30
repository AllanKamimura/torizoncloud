from .torizon_api import TorizonAPI

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

    def format_payload_info(self, payload_info):
        def format_properties(properties, indent=4):
            formatted_props = []
            for prop, details in properties.items():
                type_info = details['type']
                nullable_info = "optional" if details.get('nullable') else "required"
                format_info = f"format: {details.get('format', '')}" if 'format' in details else ""
                enum_info = f"enum: {details['enum']}" if 'enum' in details else ""
                additional_info = ", ".join(filter(None, [format_info, enum_info]))

                if type_info == 'array':
                    item_type = details['items']['type']
                    item_format = f"format: {details['items'].get('format', '')}" if 'format' in details['items'] else ""
                    formatted_props.append(
                        f"{' ' * indent}{prop:<20} ({type_info:<7}, {nullable_info}): {item_type}, {item_format}")
                else:
                    formatted_props.append(
                        f"{' ' * indent}{prop:<20} ({type_info:<7}, {nullable_info}): {additional_info}")

                valid_payload.append(prop)

                if 'properties' in details:
                    formatted_props.append(format_properties(details['properties'], indent + 4))
            return "\n".join(formatted_props)

        def format_schema(schema):
            formatted_schema = []
            if schema['type'] == 'object':
                formatted_schema.append("    Object properties:")
                if 'required' in schema:
                    for req in schema['required']:
                        if req in schema['properties']:
                            schema['properties'][req]['nullable'] = False
                if 'properties' in schema:
                    formatted_schema.append(format_properties(schema['properties'], 6))
            elif schema['type'] == 'array':
                item_type = schema['items']['type']
                nullable_info = "optional" if schema['items'].get('nullable') else "required"

                item_format = f"format: {schema['items'].get('format', '')}" if 'format' in schema['items'] else ""
                formatted_schema.append("    Object properties:")
                formatted_schema.append(f"      {'devices':<20} ({item_type:<7}, {nullable_info}): {item_format}")
                valid_payload.append('devices')

            elif schema['type'] == 'string' and 'format' in schema:
                formatted_schema.append(f"    String ({schema['format']}):")
            else:
                formatted_schema.append(f"    {schema['type'].capitalize()}:")

            return "\n".join(formatted_schema)

        formatted_payloads = []
        valid_payload = []

        for content_type, schema in payload_info.items():
            formatted_payloads.append(format_schema(schema))

        return "\n".join(formatted_payloads), valid_payload

    def format_responses(self, response):
        formatted_response = "Response:"
        description = response['description']
        contents = response.get('content', {})
        accepts_header = "application/json"

        for accepts_header, content in contents.items():
            schema = content['schema']
            properties = schema.get('properties', {})
            required = schema.get('required', [])

            formatted_response += f" {accepts_header}:\n      Object properties:"
            for prop, prop_details in properties.items():
                prop_type = prop_details.get('type', "")
                nullable = prop_details.get('nullable', False)
                optional_or_always = 'optional' if nullable else 'always'
                format_type = f", format: {prop_details['format']}" if 'format' in prop_details else ""
                enum_values = f", enum: {prop_details['enum']}" if 'enum' in prop_details else ""

                if prop_type == 'array':
                    item_type = prop_details['items']['type']
                    item_format = f", format: {prop_details['items']['format']}" if 'format' in prop_details['items'] else ""
                    formatted_response += f"\n          {prop:<20} ({'array':<7}, {optional_or_always:<8}): type: {item_type}{item_format}"
                else:
                    formatted_response += f"\n          {prop:<20} ({prop_type:<7}, {optional_or_always:<8}): {enum_values}"



        return formatted_response, accepts_header

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

            for htpp_method, endpoint_info in endpoint.items():

                docstring = f"""\n
{endpoint_info["description"]}
"""
                valid_parameters = []
                if "parameters" in endpoint_info.keys():
                    parameter_string = ""

                    for parameter in endpoint_info["parameters"]:
                        parameter["name"] = parameter["name"].replace("-", "")
                        valid_parameters.append(parameter["name"])

                        required = "required" if parameter["required"] else "optional"
                        schema = parameter["schema"].copy()
                        del schema["type"]
                        schema_str = ", ".join([f"{key}: {value}" for key, value in schema.items()])

                        parameter_string += f'\t{parameter["name"]:<20} ({parameter["schema"]["type"]:<7}, {required:<8}): {schema_str}\n'

                    parameters_string = f"""
Parameters:
{parameter_string}
"""
                    docstring += parameters_string + "\n\n"

                valid_payload = []
                if "requestBody" in endpoint_info.keys():
                    for content_type, request_body in endpoint_info["requestBody"]["content"].items():

                        formatted_payload_info, valid_payload = self.format_payload_info(request_body)
                        body_string = f"""
Content-Type: {content_type}
{formatted_payload_info}
"""

                        if content_type == "application/octet-stream":
                            valid_payload.append("data")
                            body_string += """
    with open(file, "r") as f:
        data = f.read()
"""
                            
                    docstring += body_string + "\n\n"

                endpoint_function = endpoint_info["operationId"].replace("-", "_")

                if "responses" in endpoint_info.keys():
                    for http_code, http_value in endpoint_info["responses"].items():
                        responses_string, accepts_header = self.format_responses(http_value)

                        break

                    docstring += responses_string + "\n\n"

                if htpp_method == "get":
                    method = TorizonAPI.get_func
                    create_func = TorizonAPI.create_get

                    setattr(TorizonAPI,
                            endpoint_function,
                            create_func(
                                self.api,
                                method = method,
                                api_endpoint = endpoint_path,
                                valid_params = valid_parameters,
                                func_name = endpoint_function,
                                docstring = docstring,
                                accepts_header = accepts_header))

                elif htpp_method == "post":
                    method = TorizonAPI.post_func
                    create_func = TorizonAPI.create_post

                    setattr(TorizonAPI,
                            endpoint_function,
                            create_func(
                                self.api,
                                method = method,
                                api_endpoint = endpoint_path,
                                valid_params = valid_parameters,
                                valid_payload = valid_payload,
                                func_name = endpoint_function,
                                docstring = docstring,
                                accepts_header = accepts_header))

                elif htpp_method == "put":
                    method = TorizonAPI.get_func
                    create_func = TorizonAPI.create_get

                elif htpp_method == "patch":
                    method = TorizonAPI.get_func
                    create_func = TorizonAPI.create_get

                elif htpp_method == "delete":
                    method = TorizonAPI.get_func
                    create_func = TorizonAPI.create_get

                # Assigning the dynamically created method to the class


                endpoint_list.append(endpoint_function)

        return endpoint_list