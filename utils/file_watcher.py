import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from create_code_snapshot import create_code_snapshot

class SnapshotHandler(FileSystemEventHandler):
    def __init__(self, cooldown=2):
        self.last_snapshot = 0
        self.cooldown = cooldown
        self.file_contents = {}
        
    def handle_file_change(self, event):
        current_time = time.time()
        if current_time - self.last_snapshot < self.cooldown:
            return
            
        file_path = Path(event.src_path).resolve()
        print(f"Change detected in: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
                old_content = self.file_contents.get(str(file_path), '')
                self.file_contents[str(file_path)] = new_content
                
                # Create snapshot with diff
                create_code_snapshot(changed_file=file_path, old_content=old_content, new_content=new_content)
                self.last_snapshot = current_time
        except (UnicodeDecodeError, PermissionError):
            return
            
    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_file_change(event)
        
    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_file_change(event)

def start_watcher():
    path = Path().resolve()
    event_handler = SnapshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=True)
    observer.start()
    
    try:
        print(f"Started watching directory: {path}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping file watcher...")
    
    observer.join()

if __name__ == "__main__":
    start_watcher() 