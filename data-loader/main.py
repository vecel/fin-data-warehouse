import signal
import logging
from threading import Event
from src.db.connection import build_engine
from src.loader.loader import load_all
from src.watcher.watcher import StagingDirectoryWatcher

from config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    engine = build_engine()

    load_all(engine)

    stop_event = Event()

    watcher = StagingDirectoryWatcher(
        staging_dir=config.STAGING_DIRECTORY,
        on_settled=lambda: load_all(engine),
    )


    def _shutdown(sig, frame):
        logger.info('Shutting down watcher')
        watcher.stop()
        stop_event.set()

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)
    
    watcher.start()

    logger.info('Data loader is running. Press Ctrl+C to stop')
    stop_event.wait()