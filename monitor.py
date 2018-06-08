# Monitor - Watches for changes in directories
#
# Written by Michael Kersting Jr.
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Buffer for events to be read
events_buffer = list()

#
#
# Monitor Handler Class
class MonitorHandler(PatternMatchingEventHandler):
    patterns = ["*.mkv", "*.mp4"]

    def process(self, event):
        global events_buffer
        event_data = {
            "type":event.event_type,
            "is_dir":event.is_directory,
            "location":event.src_path
            }
        events_buffer.append(dict(event_data))

    def on_deleted(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
#
#
# Get Event - Returns the oldest event and removes it from the buffer
def get_event():
    if len(events_buffer) > 0:
        return events_buffer.pop()
    else:
        return None

#
#
# Peek Event - Returns the oldest event without removing it from the buffer
def peek_event():
    if len(events_buffer) > 0:
        return events_buffer[0]
    else:
        return None

#
#
# Monitor Function - Adds a path to be monitored
def monitor(path, recursive=True):
    # Create an observer thread for the given path
    observer = Observer()
    observer.schedule(MonitorHandler(), path=path, recursive=recursive)
    observer.daemon = True
    observer.start()
