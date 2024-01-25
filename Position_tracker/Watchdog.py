import time
import Watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.pacote = None  # Initialize pacote variable

    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith(".txt"):
            print(f"Novo arquivo criado: {event.src_path}")
            self.pacote = event.src_path  # Save the file name in pacote variable

def vigiar_pasta(pasta):
    global event_handler 
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

# Access the pacote variable outside the observer loop if needed
print(f"Último arquivo criado: {event_handler.pacote}")
