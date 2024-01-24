import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith(".txt"):
            print(f"Novo arquivo criado: {event.src_path}")
            try:
                with open(event.src_path, "r") as file:
                    content = file.read()
                    print(f"Conteúdo do arquivo:\n{content}")
            except Exception as e:
                print(f"Erro ao ler o arquivo: {e}")

    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith(".txt"):
            print(f"Arquivo modificado: {event.src_path}")
            try:
                with open(event.src_path, "r") as file:
                    content = file.read()
                    print(f"Novo conteúdo do arquivo:\n{content}")
            except Exception as e:
                print(f"Erro ao ler o arquivo: {e}")

def vigiar_pasta(pasta):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, pasta, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    pasta_vigilancia = "C:\\Users\\Digital Twin\\Documents\\GitHub\\DEMO_DT\\Position_tracker\\Logs"
    vigiar_pasta(pasta_vigilancia)

