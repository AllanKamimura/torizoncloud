# TorizonCloud Python API

## About

TorizonCloud Python API is a wrapper around the [official Torizon Cloud API](https://app.torizon.io/api/docs/#/). 

The purpose of this API is to make it easier to the user by:
- Creating a login function, so the user don't need to pass the credentials at each API call
- Format the HTTP header, this can be quite challenging
- Access all devices, packages, fleets and lockboxes with the same syntax.
  - The official API creates a new endpoint for each newly created device, package, ....

## How to use
Check the [main.py](main.py) script, it should be self-explanatory.

But you simply need to:
1. Clone the repo
   1. ```git clone https://github.com/AllanKamimura/torizoncloud.git```
2.  Install the dependencies.
    1.  ```pip install -r requirements.txt```
3. Login using your [Torizon Cloud Credentials](https://developer.toradex.com/torizon/torizon-platform/torizon-api#1-create-an-api-client).
   1. It expects 2 enviroment variables, `TORIZON_CLOUD_CLIENT` and `TORIZON_CLOUD_SECRET`.
4. Check the helper function for the API endpoints.

## Examples

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

### Create a new device
```python
cloud.api.postDevices(
    deviceName = "Delicious-Hamburger", # user-defined name
    deviceId = "1234", # user-defined string
    hibernated = True)
```

This is going to return the `device_credentials.zip` for the device to connect to your cloud. 
1. dump the zip content to `/var/sota/import` in the device
2. run in the device `sudo systemctl restart aktualizr`


### 