import os
from torizon_cloud import TorizonCloud

client_id = os.getenv("TORIZON_CLOUD_CLIENT")
client_secret = os.getenv("TORIZON_CLOUD_SECRET")

cloud = TorizonCloud()
cloud.login(client_id, client_secret)

# create a new package 
compose_file_lock = "examples/camera.lock.yaml"
version = "999"

with open(compose_file_lock, "r") as f:
    data = f.read()

new_package_info = cloud.api.postPackages(    
    name           = os.path.basename(compose_file_lock),
    version        = version,
    hardwareId     = "docker-compose",
    targetFormat   = "BINARY",
    ContentLength  = os.path.getsize(compose_file_lock),
    data = data) # returns a json with package metadata

# check if the new package was correctly uploaded
assert new_package_info["size"] == os.path.getsize(compose_file_lock), "postPackages local and uploaded sizes don't match"

cloud.api.postUpdates(
    packageIds = [f"{os.path.basename(compose_file_lock)}-{version}"],
    # devices    = ["4af561db-b4a0-4346-949b-c20d5added07"], # the device must have been seen online at least 1 time
    # fleets     = ["8b96056e-0607-4e48-a098-e8c182647171"], # the device must have been seen online at least 1 time
)