import pyopencl as cl
import pyopencl.array

platforms = cl.get_platforms()
for platform in platforms:
    print("Platform:", platform.name)
    devices = platform.get_devices()
    for device in devices:
        print("Device:", device.name)