import os
from torizon_cloud import TorizonCloud

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)

print("Endpoints List:")
for endpoint in cloud.endpoint_list:
    print(f"\t{endpoint}")

print("\nUse help(cloud.api.ENDPOINT_NAME) to see the endpoint description, accepted parameters and returns")

#help(cloud.api.postDevices)