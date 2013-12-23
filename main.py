"""

Usage:
python main.py channel_name file.log

"""

# twisted imports
from twisted.internet import reactor
from twisted.python import log

# system imports
import sys

import settings.irc as settings

from models.bot_factory import BotFactory

if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)

    # create factory protocol and application
    factory_bot = BotFactory(sys.argv[1], sys.argv[2])

    # connect factory to this host and port
    reactor.connectTCP(settings.IRC_SERVER, settings.IRC_PORT, factory_bot)

    # run bot
    reactor.run()