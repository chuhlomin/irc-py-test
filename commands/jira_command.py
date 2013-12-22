import re
from jira.client import JIRA
from commands.command_abstract import CommandAbstract

import settings.jira as settings

options = {'server': 'https://jira.dengionline.com'}
basic_auth = (settings.JIRA_USER, settings.JIRA_PASSWORD)


class JiraCommand(CommandAbstract):
    def __init__(self):
        self.jira = JIRA(options, basic_auth)


    def process_command(self, command):
        mapper = [
            ('^task (.+)-([0-9]+)$', self.get_task_title),
            ('^task (.+)-([0-9]+) full$', self.get_task_full)
        ]

        for map in mapper:
            match = re.match(map[0], command)
            if match:
                method = map[1]
                return method(match.groups(1, 0))

        return 'command not found (%s)' % command


    def get_task_title(self, **args):
        issue = self.jira.issue(args[0])
        return issue.fields.summary.encode('utf-8')

    def get_task_full(self, **args):
        pass