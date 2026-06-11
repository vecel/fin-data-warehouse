import yfinance
import logging
import argparse

from src.scheduler.scheduler import build

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v',
    '--verbose',
    default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Set logging level (default: INFO)',
)
parser.add_argument(
    '-c',
    '--yfcache',
    default='./.yfcache',
    help='Set yfinance cache directory location (default: ./yfcache)'
)
args = parser.parse_args()

logging.basicConfig(
    level=getattr(logging, args.verbose),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)
yfinance.set_tz_cache_location(args.yfcache)

logger = logging.getLogger(__name__)

if __name__ == "__main__":  
    scheduler = build()
    scheduler.start()