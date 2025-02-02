import sys
import os
from subprocess import Popen
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_function):
        super().__init__()
        self.restart_function = restart_function

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print(f"Change detected in: {event.src_path}. Restarting bot...")
            self.restart_function()

def restart_bot():
    global process
    if process:
        process.kill()
    process = Popen([sys.executable, "add_member.py"])  # Replace "bot.py" with your main bot file name

if __name__ == "__main__":
    path = "."  # Watch the current directory
    process = None
    restart_bot()

    event_handler = RestartHandler(restart_bot)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        if process:
            process.kill()
