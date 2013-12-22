import time
from twisted.words.protocols import irc
from commands.command_factory import CommandFactory
from models.logger import Logger

import settings.irc as settings

class Bot(irc.IRCClient):
    nickname = settings.NICK

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = Logger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" %
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" %
                        time.asctime(time.localtime(time.time())))
        self.logger.close()


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "I'm not ready for private conversations"
            self.msg(user, msg)
            return

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "%s: I understand only certain commands (try !commands)" % user
            self.msg(channel, msg)
            self.logger.log("<%s> %s" % (self.nickname, msg))
            return

        if msg[0] == '!':
            command_raw = msg[1:].strip().split(' ', 1)
            command = CommandFactory.get_command(command_raw[0])
            if not command:
                self.msg(channel, "%s: I do not know this command" % user)
            else:
                try:
                    result = command.process_command(command_raw[1])
                    self.msg(channel, "%s: %s" % (user, result))
                except Exception as e:
                    self.msg(channel, "%s: During command execution error occurred: %s" % (user, e.__unicode__()))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))


    def alterCollidedNick(self, nickname):
        return nickname + '^'