import os
from torizon_cloud import TorizonCloud
from random import randint

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)

test_name = f"test_{randint(0, 999999)}".zfill(6)
new_device = cloud.api.postDevices(
    deviceName = test_name,
    deviceId = "12348", # user-defined string
)
assert type(new_device) == bytes, "postDevices didn't return bytes"


compose_file_lock = "examples/camera.lock.yaml"
version = "999"

with open(compose_file_lock, "r") as f:
    data = f.read()

new_package = cloud.api.postPackages(    
    name           = os.path.basename(compose_file_lock),
    version        = version,
    hardwareId     = "docker-compose",
    targetFormat   = "BINARY",
    ContentLength  = os.path.getsize(compose_file_lock),
    data = data)

assert type(new_package) == dict, "postPackages didn't return a json like"
assert "size" in new_package.keys(), "postPackages no 'size' in json"
assert new_package["size"] == os.path.getsize(compose_file_lock), "postPackages local and uploaded sizes don't match"

new_fleet = cloud.api.postFleets(
    name = test_name,
    fleetType = "static"
)

assert type(new_fleet) == str, "postFleets didn't return a uuid string"

# query a device by name
devices_by_name = cloud.api.getDevices(
    nameContains = "test_"
)

assert type(devices_by_name) == dict, "getDevices didn't return a json like"
assert "values" in devices_by_name.keys(), "getDevices no 'values' in json"

devices_uuid = [x["deviceUuid"] for x in devices_by_name["values"]]

# add the devices to the fleet
devices_uuid_reponse = cloud.api.postFleetsFleetidDevices(
    fleetId = new_fleet,
    devices = devices_uuid
)

print("postTest passed")
