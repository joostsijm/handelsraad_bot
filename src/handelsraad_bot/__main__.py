"""Main app"""

import time
import sys

from handelsraad_bot import SCHEDULER, LOGGER, telegram_bot


def main():
    """Main method"""
    LOGGER.info('starting application')
    telegram_bot.run()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()

if __name__ == '__main__':
    main()
