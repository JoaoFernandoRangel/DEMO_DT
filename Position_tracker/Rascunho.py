import time
from datetime import datetime
import paho.mqtt.client as paho
from paho import mqtt
import pyttsx3
import random 
#mude para escolher o modo de envio de mensagens para o mqtt
#ponto_fixo = "epoch"

ponto_fixo = "demo"
topico = "xyzr"

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
def current_milli_time():
    return round(time.time() * 1000)

def manda_epoch():
    global string_epoch
    epoch = current_milli_time()
    space = "%%"
    log = "log"
    string_data = "11-47-46%%223.112%%0.0%%40.082%%0.0%%GF"
    string_inicio = str(epoch) + space
    string_epoch = string_inicio + string_data + space  + str(epoch + random.randint(1,1000))     
    #print(string_epoch)

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("position_tracker", "Digital1")
client.connect("dd6e8d1cc8524360a537e7db4e5924f8.s2.eu.hivemq.cloud", 8883)
client.loop_start()

ponto_esteira = [113.0719, -177.6358, 38.6852, -75.2771]
home = [223.0752, 2.4736, 67.9859, 90]
montagem = [287.5588 , 3.0321 , 38.6762 , 10.6513]
montagemtampa = [287.0620 , 2.6663 , 56.7805 , 7.4995]
tampa1 = [190.5303 , 72.3327 , 23.4604 , 8.6788]
peca1 = [188.3365 , 178.3896 , 36.2875 , -35.9722]
data_hora_atual = datetime.now()
formato_data_hora = "%Y-%m-%d_%H-%M-%S"
global string_garra
string_garra = "GA"

space = "%%"
inicio = "log"
ponto = "."
virg = ","

def faz_string(ponto):
    epoch = current_milli_time()
    data_hora_atual = datetime.now()
    formato_data_hora = "%H-%M-%S"
    timestamp1 = data_hora_atual.strftime(formato_data_hora)
    string = str(round(ponto[0], 3)) + space + str(round(ponto[1], 3)) + space + str(
        round(ponto[2], 3)) + space + str(round(ponto[3], 3)) + space + string_garra
    string.replace(str(ponto), str(virg))
    string =  str(epoch) + space + timestamp1 + space + string + space + str(epoch + random.randint(1,200))
    
    return string

#print(faz_string(ponto_esteira))

if (ponto_fixo == "demo"):
    for i in range(100): ## printa no servidor para movimentação do robo na unity
        print(i)
        client.publish(topico, faz_string(ponto_esteira).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        string_garra = "GF"
        client.publish(topico, faz_string(home).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        #print(faz_string(home))
        client.publish(topico, faz_string(montagem).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        string_garra = "GA"
        client.publish(topico, faz_string(montagemtampa).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        client.publish(topico, faz_string(tampa1).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        client.publish(topico, faz_string(peca1).replace(str(ponto), str(virg)), 1)
        string_garra = "GF"
        time.sleep(3)
        client.publish(topico, faz_string(ponto_esteira).replace(str(ponto), str(virg)), 1)
        time.sleep(3)
        string_garra = "GA"
        client.publish(topico, faz_string(home).replace(str(ponto), str(virg)), 1)
else:
    for i in range(500):
        manda_epoch()
        client.publish(topico, string_epoch, 1)
        print(string_epoch)
        #print(string_epoch)
        epoch = current_milli_time()
        time.sleep(1)

    

