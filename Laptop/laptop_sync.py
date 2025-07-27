from kuksa_client.grpc import VSSClient, Datapoint
import time

client_to_rpi = VSSClient('192.168.0.105', 55555)
client_local = VSSClient('localhost', 55555)

client_to_rpi.connect()
client_local.connect()

while True:
    try:
        print("[Laptop Sync] Getting local Laptop values")
        laptop_values = client_local.get_current_values([
            'Vehicle.Camera.Laptop.Image',
            'Vehicle.Camera.Laptop.ObjectCount'
        ])
        laptop_image = laptop_values['Vehicle.Camera.Laptop.Image'].value
        laptop_count = laptop_values['Vehicle.Camera.Laptop.ObjectCount'].value
        print(f"[Laptop Sync] Got local Laptop image (len={len(laptop_image)}), count={laptop_count}")

        print("[Laptop Sync] Sending to RPi")
        client_to_rpi.set_current_values({
            'Vehicle.Camera.Laptop.Image': Datapoint(laptop_image),
            'Vehicle.Camera.Laptop.ObjectCount': Datapoint(laptop_count)
        })

        print("[Laptop Sync] Getting RPi values")
        rpi_values = client_to_rpi.get_current_values([
            'Vehicle.Camera.RPi.Image',
            'Vehicle.Camera.RPi.ObjectCount'
        ])
        rpi_image = rpi_values['Vehicle.Camera.RPi.Image'].value
        rpi_count = rpi_values['Vehicle.Camera.RPi.ObjectCount'].value
        print(f"[Laptop Sync] Got RPi image (len={len(rpi_image)}), count={rpi_count}")

        print("[Laptop Sync] Writing RPi values to local DB")
        client_local.set_current_values({
            'Vehicle.Camera.RPi.Image': Datapoint(rpi_image),
            'Vehicle.Camera.RPi.ObjectCount': Datapoint(rpi_count)
        })

        print("[Laptop Sync] One full sync completed.")
        time.sleep(1)
    except Exception as e:
        print(f"[Laptop Sync] Error: {e}")
        time.sleep(2)
