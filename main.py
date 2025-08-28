
import os
import time
import shutil
import argparse
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def safe_move(src, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    base = os.path.basename(src)
    name, ext = os.path.splitext(base)
    dest = os.path.join(dest_dir, base)
    i = 1
    while os.path.exists(dest):
        dest = os.path.join(dest_dir, f"{name} ({i}){ext}")
        i += 1
    shutil.move(src, dest)

def get_target_folder(file_path, rules, default_folder):
    ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    folder = rules.get(ext, default_folder)
    return folder

class SortHandler(FileSystemEventHandler):
    def __init__(self, rules, default_folder, base_dir):
        self.rules = rules
        self.default_folder = default_folder
        self.base_dir = base_dir

    def on_created(self, event):
        if event.is_directory: 
            return
        self._handle(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self._handle(event.dest_path)

    def _handle(self, path):
        try:
            # Wait for file to finish downloading (best-effort)
            time.sleep(0.5)
            folder = get_target_folder(path, self.rules, self.default_folder)
            dest_dir = os.path.join(self.base_dir, folder)
            safe_move(path, dest_dir)
            print(f"Moved: {path} -> {dest_dir}")
        except Exception as e:
            print(f"Failed to move {path}: {e}")

def organize_once(base_dir, rules, default_folder):
    for entry in os.scandir(base_dir):
        if entry.is_file():
            folder = get_target_folder(entry.path, rules, default_folder)
            dest_dir = os.path.join(base_dir, folder)
            try:
                safe_move(entry.path, dest_dir)
                print(f"Moved: {entry.path} -> {dest_dir}")
            except Exception as e:
                print(f"Failed to move {entry.path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Smart File Organizer")
    parser.add_argument("--watch", help="Watch directory and sort in real-time")
    parser.add_argument("--organize", help="Organize directory once and exit")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    rules = cfg.get("rules", {})
    default_folder = cfg.get("default_folder", "Others")

    if args.organize:
        organize_once(args.organize, rules, default_folder)
        return

    if args.watch:
        base_dir = args.watch
        handler = SortHandler(rules, default_folder, base_dir)
        obs = Observer()
        obs.schedule(handler, base_dir, recursive=False)
        obs.start()
        print(f"Watching: {base_dir}. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            obs.stop()
        obs.join()
        return

    parser.print_help()

if __name__ == "__main__":
    main()
