import gps
import time
from datetime import datetime
import ssl
from paho.mqtt import client as mqttc
session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    speed = msg.payload
    serial1.write(speed)

client = mqttc.Client(client_id="123545", userdata=None, protocol=mqttc.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("raspberry", "12345678@No")
client.connect("838c210630fd4e43b295c4155e186c7b.s1.eu.hivemq.cloud", 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish





	

try:
	
    while True:
        try:
            report = session.next()
        except KeyError as e:
            print(f"Error reading GPS data: {e}")
        except StopIteration:
            print("No more GPS data or GPSD servicestopped.")
        except Exception as e:
            print(f"An unexpected error occured: {e}")
            break
        if report['class'] == 'TPV':
            
            latitude = getattr(report, 'lat', "Unknown")
            longitude = getattr(report, 'lon', "Unknown")
			#speed = getattr(report, 'speed', "Unknown")  
            time_utc = getattr(report, 'time', "Unknown")  
            serial = getattr(report, 'device', "Unknown")  
            
            gps_data = {
                "serial": serial,
                "time_utc": time_utc,
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed
            }
            gps_json = json.dumps(gps_data)
            client.publish("location", gps_data, qos=1 )

            print(f"Published to MQTT topic location: {gps_json}")

            client.loop()
            time.sleep(10)

except KeyboardInterrupt:
    # Exit the program gracefully if Ctrl+C is pressed
    print("GPS data collection stopped.")

except StopIteration:
    # Handle GPS signal loss or end of data stream
    print("GPSD has stopped.")
    
finally:
	client.disconnect()


