from kuksa_client.grpc import VSSClient, Datapoint
import time

client_to_laptop = VSSClient('192.168.0.104', 55555)
client_local = VSSClient('localhost', 55555)

client_to_laptop.connect()
client_local.connect()

while True:
    try:
        print("[RPi Sync] Getting local RPi values")
        rpi_values = client_local.get_current_values([
            'Vehicle.Camera.RPi.Image',
            'Vehicle.Camera.RPi.ObjectCount'
        ])
        rpi_image = rpi_values['Vehicle.Camera.RPi.Image'].value
        rpi_count = rpi_values['Vehicle.Camera.RPi.ObjectCount'].value
        print(f"[RPi Sync] Got local RPi image (len={len(rpi_image)}), count={rpi_count}")

        print("[RPi Sync] Sending to Laptop")
        client_to_laptop.set_current_values({
            'Vehicle.Camera.RPi.Image': Datapoint(rpi_image),
            'Vehicle.Camera.RPi.ObjectCount': Datapoint(rpi_count)
        })

        print("[RPi Sync] Getting Laptop values")
        laptop_values = client_to_laptop.get_current_values([
            'Vehicle.Camera.Laptop.Image',
            'Vehicle.Camera.Laptop.ObjectCount'
        ])
        laptop_image = laptop_values['Vehicle.Camera.Laptop.Image'].value
        laptop_count = laptop_values['Vehicle.Camera.Laptop.ObjectCount'].value
        print(f"[RPi Sync] Got Laptop image (len={len(laptop_image)}), count={laptop_count}")

        print("[RPi Sync] Writing Laptop values to local DB")
        client_local.set_current_values({
            'Vehicle.Camera.Laptop.Image': Datapoint(laptop_image),
            'Vehicle.Camera.Laptop.ObjectCount': Datapoint(laptop_count)
        })

        print("[RPi Sync] One full sync completed.")
        time.sleep(1)
    except Exception as e:
        print(f"[RPi Sync] Error: {e}")
        time.sleep(2)
