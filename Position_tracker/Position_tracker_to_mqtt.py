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

def on_disconnect(client, userdata, rc, properties=None):
    print(f"Disconnected with result code {rc}. Reconnecting...")
    client.reconnect()

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("position_tracker", "Digital1")
client.connect("dd6e8d1cc8524360a537e7db4e5924f8.s2.eu.hivemq.cloud", 8883, keepalive=5)  # Include keepalive parameter
topico = "garraxyzr"
client.publish(topico, "vai filhao", 1)

stop_observer = False  # Flag to signal observer to stop and join


class MyHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder
        self.pacote = None

    def on_created(self, event):
      
        if event.is_directory:
            return
        elif event.src_path.endswith(".txt"):
            print(f"Novo arquivo criado: {event.src_path}")
           #str_pub = event.src_path.replace("C:\\Users\\João Fernando Rangel\\Desktop\\Digital Twin\\DEMO_DT\\Position_tracker\\Logs\\log___","")
            str_pub = event.src_path.replace("C:\\Users\\Digital Twin\\Documents\\GitHub\\DEMO_DT\\Position_tracker\\Logs\\log___", "")
            print('.')
            str_pub = str_pub.replace(".txt", "")
            
            print('.......')
            client.publish(topico, str_pub, 1)
            client.loop(1,10)
            print('----------')
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
    global stop_observer
    if key == keyboard.Key.esc:
        print("Tecla Esc pressionada. Removendo arquivos e encerrando o programa.")
        delete_files_with_prefix(pasta_vigilancia, "log___")
        client.publish(topico, "Movimentação terminada", 1)
        stop_observer = True

def vigiar_pasta(pasta):
    event_handler = MyHandler(pasta)
    global observer
    observer = Observer()
    observer.schedule(event_handler, pasta, recursive=False)
    observer.start()

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while not stop_observer:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()

if __name__ == "__main__":
    pasta_vigilancia = "C:\\Users\\Digital Twin\\Documents\\GitHub\\DEMO_DT\\Position_tracker\\Logs"
    #pasta_vigilancia = "C:\\Users\\João Fernando Rangel\\Desktop\\Digital Twin\\DEMO_DT\\Position_tracker\\Logs"
    
    vigiar_pasta(pasta_vigilancia)
