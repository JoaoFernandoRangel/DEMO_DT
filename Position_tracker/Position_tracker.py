import time
import winsound
import paho.mqtt.client as paho
from paho import mqtt
import pyttsx3

def on_connect(client, userdata, flags, rc, properties=None):
    #print("CONNACK received with code %s." % rc)
    # Subscribe to the "idle_rx" topic when connected
    client.subscribe("idle_rx", qos=1)
def on_publish(client, userdata, mid, properties=None):
    print("publicado")
    #print("mid: " + str(mid))
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscrito")
    #print("Subscribed: " + str(mid) + " " + str(granted_qos))
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print("-----------")
    print(f"Mensagem recebida: {mensagem}")
    print("-----------")
    # Handle the received message here
    #display_countdown(remaining_seconds, msg.payload.decode())
 
 
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("position_tracker", "Digital1")
client.connect("dd6e8d1cc8524360a537e7db4e5924f8.s2.eu.hivemq.cloud", 8883)
topico = "Claw-POS"  

for i in range(5):
    client.publish(topico, "agora vai", 0)
    print("publicado")
    time.sleep(0.5)
