from twisted.internet import protocol, reactor
from models.bot import Bot


class BotFactory(protocol.ClientFactory):
    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename

    def buildProtocol(self, addr):
        bot = Bot()
        bot.factory = self
        return bot

    def clientConnectionLost(self, connector, reason):
        # If we get disconnected, reconnect to server.
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()