import logging
from watchdog.observers import Observer

from src.watcher.handler import StagingEventHandler

logger = logging.getLogger(__name__)


class StagingDirectoryWatcher:
    def __init__(
        self,
        staging_dir,
        on_settled,
    ):
        self._staging_dir = staging_dir
        handler = StagingEventHandler(on_settled)
        self._observer = Observer()
        self._observer.schedule(handler, path=staging_dir, recursive=True)

    def start(self):
        self._observer.start()
        logger.info(f'Watching {self._staging_dir}')

    def stop(self):
        self._observer.stop()
        self._observer.join()