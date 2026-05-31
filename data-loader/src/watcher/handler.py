import logging

from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)


class StagingEventHandler(FileSystemEventHandler):
    def __init__(self, on_settled):
        self._on_settled = on_settled

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.parquet'):
            self._on_settled()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.parquet'):
            self._on_settled()