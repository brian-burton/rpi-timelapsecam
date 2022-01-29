import paho.mqtt.client as mqtt
from gpiozero import CPUTemperature, DiskUsage

client_name = "CamPi"
broker = "dashboard.local"
topic = "matrix3/message"

client = mqtt.Client(client_name)

cputemp = CPUTemperature()
diskusage = DiskUsage()

if __name__ == "__main__":
    message = f'{{\"temperature\": {cputemp.temperature}, \"disk\": {diskusage.usage}}}'
    #print(message)
    client.connect(broker)
    client.publish.single(topic, message)
    client.disconnect()
