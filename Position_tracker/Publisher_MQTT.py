import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pynput import keyboard
import time
import paho.mqtt.client as paho
from paho import mqtt
import ntplib as ntp

pc = "jf" # Se no notebook de João usar jf
teste = 1 #se estiver em teste manter 1
link_comum = 'europe.pool.ntp.org'

pot_enable = True

#Funções para conexão em broker MQTT
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

client_ntp = ntp.NTPClient()

if (teste==1):
    topico =  "teste"
else:
    topico = "xyzr"
space = "%%"

def pega_epoch():
    response = client_ntp.request(link_comum, version = 3)
    return int(response.tx_time*1000)

class MyHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder
        self.pacote = None

    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith(".txt"):
            #print(f"Novo arquivo criado: {event.src_path}")
            if (pc == "jf"):
                str_src = event.src_path.replace("C:\\Users\\João Fernando Rangel\\Desktop\\Digital Twin\\DEMO_DT\\Position_tracker\\Logs\\log%%","")
            #Adicionar diretorio do computador de mesa
            else:
                str_src = event.src_path.replace("C:\\Users\\Digital Twin\\Documents\\GitHub\\DEMO_DT\\Position_tracker\\Logs\\log%%","")
            str_0 = str(str_src)
            print(str_0)
            str_1 = str_0.replace(".txt", "")           
            str_2 = str_1.replace(",",".")            
            splited = str_2.split('%%')
            epoch = pega_epoch()
            str_final = str_2 + space + str(epoch)
            print(str_final)
            #str_pub = str_pub.replace("-", ":")
            print(str_final)
            client.publish(topico, str_final, 1)
            self.pacote = event.src_path

def delete_files_with_prefix(folder, prefix):
    for file_name in os.listdir(folder):
        if file_name.startswith(prefix) and file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover o arquivo {file_path}: {e}")

def on_press(key):
    if key == keyboard.Key.esc:
        print("Tecla Esc pressionada. Removendo arquivos e encerrando o programa.")
        delete_files_with_prefix(pasta_vigilancia, "log%%")
        #client.publish(topico, "Movimentação terminada", 1)
        #observer.stop()

def vigiar_pasta(pasta):
    event_handler = MyHandler(pasta)
    global observer
    observer = Observer() 
    observer.schedule(event_handler, pasta, recursive=False)
    observer.start()
    client.loop_start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

# observer.join()  # Remova esta linha para permitir que o programa continue após a remoção dos arquivos


if __name__ == "__main__":
    if pc == "jf":
        pasta_vigilancia = "C:\\Users\\João Fernando Rangel\\Desktop\\Digital Twin\\DEMO_DT\\Position_tracker\\Logs"
    else:
        pasta_vigilancia = "C:\\Users\\Digital Twin\\Documents\\GitHub\\DEMO_DT\\Position_tracker\\Logs"
    client.publish(topico, "a", 1)
    vigiar_pasta(pasta_vigilancia)
    




