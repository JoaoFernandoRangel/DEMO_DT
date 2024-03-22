import ntplib as ntp
import datetime as dt
import time
import paho.mqtt.client as paho
from paho import mqtt


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

client_ntp = ntp.NTPClient()



while True:
    #time.sleep(5)
    response = client_ntp.request('europe.pool.ntp.org', version=3)
    time.sleep(5)
    response1 = client_ntp.request('europe.pool.ntp.org', version=3)

    epoch_time_before = response.tx_time*1000 #transforma para milissegundos
    epoch_time_after = response1.tx_time*1000
    print("----")
    print(epoch_time_before, " menos ", epoch_time_after, " = ", epoch_time_after-epoch_time_before, "_milissegundos")
    string = epoch_time_before, " menos ", epoch_time_after, " = ", epoch_time_after-epoch_time_before, "_milissegundos"
    client.publish("abc", str(string), qos = 1)
    print("---- ", i)
    i = i + 1
