import os
from build.sensor_pb2 import Sensor

if __name__ == "__main__":
    with open(os.path.join("build", "sensor.data"), 'rb') as file:
        content = file.read()
        print("Retrieve Sensor object from sensor.data")
        sensor = Sensor()
        sensor.ParseFromString(content)
        door = "Open" if sensor.door else "Closed"
        print(f"Sensor name: {sensor.name}")
        print(f"Sensor temperature: {sensor.temperature}")
        print(f"Sensor humidity: {sensor.humidity}")
        print(f"Sensor door: {door}")
