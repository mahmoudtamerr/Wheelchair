from paho.mqtt import client as mqttc
from paho import mqtt
import serial
import time
arduino_port2 = serial.Serial('/dev/ttyACM1', 19200)
time.sleep(2)
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
def on_publish(client, userdata, mid, properties=None):
    pass
client = mqttc.Client(client_id="7553392", userdata=None, protocol=mqttc.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("raspberry", "12345678@No")
client.connect("b32caacf49864326847d6cbb1722c04c.s1.eu.hivemq.cloud", 8883)
client.on_publish = on_publish
while True:
     response= arduino_port2.readline().decode().strip()
     print("Response:",response)
     if (response== "the chair is stable " or response == :"Warning: Chair is turning or turned over!"):
         
        client.publish("notification", payload= response, qos=1)
        print(f"Published to MQTT topic location: {response}")
     client.loop()
     time.sleep(2)
