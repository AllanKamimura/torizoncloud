# TorizonCloud Python API

## About

TorizonCloud Python API is a wrapper around the [official Torizon Cloud API](https://app.torizon.io/api/docs/#/). 

The purpose of this API is to make it easier to the user by:
- Creating a login function, so the user don't need to pass the credentials at each API call
- Format the HTTP header, this can be quite challenging
- Access all devices, packages, fleets and lockboxes with the same syntax.
  - The official API creates a new endpoint for each newly created device, package, ....

## How to use
Check the [examples/main.py](examples/main.py) script, it should be self-explanatory.

But you simply need to:
1. Install the package
   1. ```pip install torizon-cloud```
2. Login using your [Torizon Cloud Credentials](https://developer.toradex.com/torizon/torizon-platform/torizon-api#1-create-an-api-client).
   1. It expects 2 enviroment variables, `TORIZON_CLOUD_CLIENT` and `TORIZON_CLOUD_SECRET`.
3. Check the helper function for the API endpoints.

## Simple Examples

Check the [examples folder](examples) for some common use cases.

### Login into the platform
```python
import os
from torizon_cloud import TorizonCloud

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)
```

### Get a list of the provisioned devices
```python
cloud.api.getDevices()
```

### Get a list of uploaded Packages
```python
cloud.api.getPackages()
```

### Get a list of created fleets
```python
cloud.api.getFleets()
```

### Get a list of created Lockboxes
```python
cloud.api.getLockboxes()
```

### Get a list of created Lockboxes with details
```python
cloud.api.getLockbox_details()
```

### Get a list of metric names
```python
cloud.api.getDevice_dataMetric_names()
```

### Get Network info about devices
This is going to return info about ['deviceUuid', 'localIpV4', 'hostname', 'macAddress']
```python
cloud.api.getDevicesNetwork()
```

### Get information about the Packages instaled on a device
```python
cloud.api.getDevicesPackagesDeviceuuid(
    deviceUuid = '558c5227-62fe-4a83-beea-7153d7ae641d' # you can get this from getDevices
)
```

### Post create a new device
```python
cloud.api.postDevices(
    deviceName = "Delicious-Hamburger", # user-defined name
    deviceId   = "1234", # user-defined string
    hibernated = True)
```

This is going to return the `device_credentials.zip` for the device to connect to your cloud. 
1. dump the zip content to `/var/sota/import` in the device
2. run in the device `sudo systemctl restart aktualizr`


### Post upload a new package
```python
compose_file_lock = "examples/camera.lock.yaml"
version = "999"

with open(compose_file_lock, "r") as f:
    data = f.read()

cloud.api.postPackages(    
    name           = os.path.basename(compose_file_lock),
    version        = version,
    hardwareId     = "docker-compose",
    targetFormat   = "BINARY",
    ContentLength  = os.path.getsize(compose_file_lock),
    data = data)
```

### Post create a new fleet
```python
new_fleet_uuid = cloud.api.postFleets(
    name = "test",
    fleetType = "static"
) # returns a string with the fleet uuid
```

### Post add devices to the fleet
```python
# query a device by name
devices_by_name = cloud.api.getDevices(
    nameContains = "Delicious-Hamburger"
)["values"] # returns a list of devices with nameContains

devices_uuid = [x["deviceUuid"] for x in devices_by_name["values"]]

# add the devices to the fleet
devices_uuid_reponse = cloud.api.postFleetsFleetidDevices(
    fleetId = new_fleet_uuid,
    devices = devices_uuid
)
```

### Post an update to a list of devices or list of fleets
```python
cloud.api.postUpdates(
    packageIds = [f"{os.path.basename(compose_file_lock)}-{version}"],
    # devices    = ["4af561db-b4a0-4346-949b-c20d5added07"], # the device must have been seen online at least 1 time
    # fleets     = ["8b96056e-0607-4e48-a098-e8c182647171"], # the device must have been seen online at least 1 time
)
```
