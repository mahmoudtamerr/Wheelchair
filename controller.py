import serial
import time
from pyPS4Controller.controller import Controller
import ssl
from paho.mqtt import client as mqttc
from paho import mqtt
arduino_port = serial.Serial('/dev/ttyACM0', 9600)
baud_rate=9600
time.sleep(2)
setup = 0
def send_command(command):
	arduino_port.write(command.encode())
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
def on_message(client, userdata, msg):
	global setup
	if msg.topic == "control":
		print(f"Received message from control topic: {msg.payload.decode()}")
		send_command(msg.payload.decode())  # Example: control command to move forward
	elif msg.topic == "setup_control":
		setup_value = int(msg.payload.decode())
		print(f"Received setup value: {setup_value}")
		setup = setup_value  # Update the setup value based on the message
		print(f"Received setup2 value: {setup}")

client = mqttc.Client(client_id="11558", userdata=None, protocol=mqttc.MQTTv5)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("mahmoud", "12345678@Nu")
client.connect("b32caacf49864326847d6cbb1722c04c.s1.eu.hivemq.cloud", 8883)
client.subscribe("control", qos=1)
client.subscribe("setup_control", qos=1)

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
	#move the robot forward
    def on_up_arrow_press(self):
        command="f"
        send_command(command)
	#stop the robot	
    def on_up_down_arrow_release(self):
        command="s"
        send_command(command)
	#move the robot backward
    def on_down_arrow_press(self):
        command="b"
        send_command(command)
	#move the robot right
    def on_right_arrow_press(self):
        command="r"
        send_command(command)
	#stop the robot
    def on_left_right_arrow_release(self):
        command="s"
        send_command(command)
	#move the robot left
    def on_left_arrow_press(self):
        command="l"
        send_command(command)    

while True:
	client.loop_start()
	if( setup == 1):
		print("Running in PS4 controller mode")
		controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
	# you can start listening before controller is paired, as long as you pair it within the timeout window
		controller.listen(timeout=60)		
	elif (setup == 0):
		print("Running in MQTT mode")
	client.loop_stop() 
