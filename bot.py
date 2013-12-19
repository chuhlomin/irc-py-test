from socket import *
from jira.client import JIRA

HOST = '137.116.220.12'
PORT = 6667

NICK_NAME = "bot-py"
USER_NAME = "Test Bot"
REAL_NAME = "Test Bot (really)"
HOST_NAME = ""
SERVER_NAME = "DengiOnlineNet"

options = {
    'server': 'https://jira.dengionline.com',
}

basic_auth = ('chuhlomin', '')

jira = JIRA(options, basic_auth)


class Irc_wrapper:
    def __init__(self, host, port, nick_name, user_name, host_name, server_name, real_name):
        self.data = ''
        self.host = host
        self.port = port

        self.irc = socket(AF_INET, SOCK_STREAM)

        self.init_irc()
        self.nick(nick_name)
        self.user(user_name, host_name, server_name, real_name)

    def init_irc(self):
        self.irc.connect((self.host, self.port))

    def read_data(self):
        self.data = self.irc.recv(4096)

    def find_in_data(self, string):
        if (self.data.find(string) != -1):
            return True

        return False

    def command(self, command):
        self.irc.send(command)

    def private_message(self, message):
        self.command("PRIVMSG %s\r\n" % message)

    def join(self, channel_name):
        self.command("JOIN #%s\r\n" % channel_name)

    def nick(self, nick_name):
        self.command("NICK %s\r\n" % nick_name)

    def user(self, user_name, host_name, server_name, real_name):
        self.command("USER %s %s %s :%s\r\n" % (user_name, host_name, server_name, real_name))

    def pong(self, data):
        self.command("PONG %s\r\n" % data)


irc_client = Irc_wrapper(HOST, PORT, NICK_NAME, USER_NAME, HOST_NAME, SERVER_NAME, REAL_NAME)

while True:

    irc_client.read_data()
    print irc_client.data

    if irc_client.find_in_data('PING'):
        irc_client.pong(irc_client.data.split()[1])

    elif irc_client.find_in_data('INVITE'):
        channel = irc_client.data.split('#')[-1]
        irc_client.join(channel)

    elif irc_client.find_in_data('PRIVMSG'):

        message = ':'.join(irc_client.data.split(':')[2:])

        if message.lower().find('%ans') == 0:

            nick = irc_client.data.split('!')[0].replace(':', '')
            destination = ''.join(irc_client.data.split(':')[:2]).split(' ')[-2]
            function = message.split(' ')[1]

            try:
                solution = str(eval(function))
            except:
                solution = "Wrong Input. Check Again!"

            message = destination + " :" + nick + ": " + solution
            irc_client.private_message(message)

        elif message.lower().find('%jira-task-title') == 0:

            nick = irc_client.data.split('!')[0].replace(':', '')
            destination = ''.join(irc_client.data.split(':')[:2]).split(' ')[-2]
            task = message.split(' ')[1].rstrip('\r\n')

            try:
                issue = jira.issue(task)
                task_title = issue.fields.summary.encode('utf-8')
            except:
                task_title = 'Some error...'

            message = destination + " :" + nick + ": " + task_title

            irc_client.private_message(message)


irc_client.irc.close()