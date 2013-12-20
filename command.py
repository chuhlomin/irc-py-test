__author__ = 'k.chukhlomin@gmail.com'


class JiraCommand:
    def process_command(self, command):
        return "_".join(command) + ' <- wtf?'

    # issue = jira.issue(task)
    # task_title = issue.fields.summary.encode('utf-8')

    # from jira.client import JIRA
    # options = { 'server': 'https://jira.dengionline.com' }
    # basic_auth = ('chuhlomin', '')
    # jira = JIRA(options, basic_auth)

class CommandFactory(object):
    objects = {
        'jira': JiraCommand,
        #'jenkins': JenkinsCommand,
        #'vote': VoteCommand,
    }

    def get_command(self, name='jira'):
        if name not in self.objects.keys():
            return None

        return self.objects[name]()