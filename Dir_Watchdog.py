from watchdog.observers import Observer
from watchdog.events import *
from PDFRenamer import rename
import time,sys,os
import os.path

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))
            filename=event.dest_path
            extension = os.path.splitext(filename)[1]
            if extension=='.pdf':
                print(filename)
                rename(filename)

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))

        else:
            print("file created :{0}".format(event.src_path))
            filename=event.src_path
            extension = os.path.splitext(filename)[1]
            if extension=='.pdf':
                print(filename)
                rename(filename)

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,sys.argv[1],True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()