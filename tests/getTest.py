import os
from torizon_cloud import TorizonCloud

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)

devices  = cloud.api.getDevices()
assert type(devices) == dict, "getDevices didn't return a json like"
assert "values" in devices.keys(), "getDevices no 'values' in json"

packages = cloud.api.getPackages()
assert type(packages) == dict, "getPackages didn't return a json like"
assert "values" in packages.keys(), "getPackages no 'values' in json"

fleets   = cloud.api.getFleets()
assert type(fleets) == dict, "getFleets didn't return a json like"
assert "values" in fleets.keys(), "getFleets no 'values' in json"

device_packages = cloud.api.getDevicesPackages()
assert type(device_packages) == dict, "getDevicesPackages didn't return a json like"
assert "values" in device_packages.keys(), "getDevicesPackages no 'values' in json"

device_networks = cloud.api.getDevicesNetwork()
assert type(device_networks) == dict, "getDevicesNetwork didn't return a json like"
assert "values" in device_networks.keys(), "getDevicesNetwork no 'values' in json"

lockboxes = cloud.api.getLockboxes()
assert type(lockboxes) == list, "getLockboxes didn't return a list like"

lockboxes_detailed = cloud.api.getLockbox_details()
assert type(lockboxes_detailed) == dict, "getLockbox_details didn't return a json like"

datametrics_names = cloud.api.getDevice_dataMetric_names()
assert type(datametrics_names) == dict, "getDevice_dataMetric_names didn't return a json like"
assert "values" in datametrics_names.keys(), "getDevice_dataMetric_names no 'values' in json"
