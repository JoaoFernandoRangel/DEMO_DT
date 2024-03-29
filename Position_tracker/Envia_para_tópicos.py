import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynput import keyboard
import time
import winsound
import paho.mqtt.client as paho
from paho import mqtt
import pyttsx3

def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe("idle_rx", qos=1)

def on_publish(client, userdata, mid, properties=None):
    print("publicado")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscrito")

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    print("-----------")
    print(f"Mensagem recebida: {mensagem}")
    print("-----------")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}. Reconnecting...")
    client.reconnect()

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("position_tracker", "Digital1")
#client.username_pw_set("User_pc", "Digital1#")
client.connect("dd6e8d1cc8524360a537e7db4e5924f8.s2.eu.hivemq.cloud", 8883) #client DT
#client.connect("25d06c5109f94ef78c7bcfc1c33fdf20.s2.eu.hivemq.cloud", 8883) #client sitio
topico = "garraxyzr" 
i = 0

client.loop_start()  # Run the loop in the background

try:
    while True:
        string = "vai filhao" + str(i)
        client.publish(topico, string, qos=1)
        time.sleep(0.5)
        i = i + 1
except KeyboardInterrupt:
    print("Exiting the loop.")
    client.loop_stop()  # Stop the loop before exiting
    client.disconnect()

