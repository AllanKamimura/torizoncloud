import os
from torizon_cloud import TorizonCloud

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)

# create a new device
new_device_name = "Delicious-Hamburger"
new_device_credentials = cloud.api.postDevices(
    deviceName = new_device_name, # user-defined name
    deviceId   = "1234", # user-defined string
    hibernated = True) # returns a binary data with a .zip credentials

with open(f"{new_device_name}_credentials.zip", "wb+") as f:
    f.write(new_device_credentials) # we need to, somehow, pass this to the device 

# create a new fleet
new_fleet_uuid = cloud.api.postFleets(
    name = "test",
    fleetType = "static"
) # returns a string with the fleet uuid


# query a device by name
devices_by_name = cloud.api.getDevices(
    nameContains = "Delicious-Hamburger"
)["values"] # returns a list of devices with nameContains

devices_uuid = [x["deviceUuid"] for x in devices_by_name]

# add the devices to the fleet
devices_uuid_reponse = cloud.api.postFleetsFleetidDevices(
    fleetId = new_fleet_uuid,
    devices = devices_uuid
)

