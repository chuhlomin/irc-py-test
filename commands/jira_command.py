import re
from jira.client import JIRA
from commands.command_abstract import CommandAbstract

import settings.jira as settings

options = {'server': settings.JIRA_SERVER}
basic_auth = (settings.JIRA_USER, settings.JIRA_PASSWORD)


class JiraCommand(CommandAbstract):
    def __init__(self):
        self.jira = JIRA(options, basic_auth)

    def help(self):
        return {
            'task JRA-11': 'title of task',
            'task JRA-12 full': 'detailed information about task',
            'jql summary ~ text and assignee = b.godunov@mail.ru': 'JQL search'
        }

    def process_command(self, command):
        mapper = [
            ('^task ([A-Z]+-[0-9]+)$', self.get_task_title),
            ('^task ([A-Z]+-[0-9]+) full$', self.get_task_full),
            ('^jql (.+)', self.get_jql_result)
        ]

        for map in mapper:
            match = re.match(map[0], command)
            if match:
                method = map[1]
                try:
                    return method(match.groups()).encode('utf-8')
                except Exception as e:
                    return 'exception: %s' % e.__unicode__()

        return 'command not found (%s)' % command

    def get_issue(self, args):
        issue_id = args[0]
        return self.jira.issue(issue_id)

    def get_task_title_by_issue(self, issue):
        return "%s %s %s" % \
               (self.get_status_abbr(str(issue.fields.status)),
                issue.key,
                issue.fields.summary)

    def get_task_title(self, args):
        issue = self.get_issue(args)
        return self.get_task_title_by_issue(issue)

    def get_task_full(self, args):
        issue = self.get_issue(args)
        versions = [str(version) for version in issue.fields.fixVersions]

        result = self.get_task_title_by_issue(issue)
        result += "\n     Assignee: %s. Reporter: %s" % \
                  (issue.fields.assignee.name,
                   issue.fields.reporter.name)
        result += "\n     FixVersions: %s" % ' '.join(versions)

        return result

    def get_jql_result(self, args):
        issues = self.jira.search_issues(args[0])
        result = ''
        for issue in issues:
            status_abbr = self.get_status_abbr(str(issue.fields.status))
            result += '%s %s %s\n' % (status_abbr, issue.key, issue.fields.summary)

        return result

    def get_status_abbr(self, status):
        words = status.split(' ')
        abbr = ''
        for word in words:
            abbr += word[0]

        if len(abbr) < 2:
            abbr += status[1]

        return '[' + abbr + ']'