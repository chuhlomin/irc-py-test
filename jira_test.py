# https://bitbucket.org/bspeakmon/jira-python
# sudo pip install jira-python

from jira.client import JIRA

options = {
    'server': 'https://jira.dengionline.com',
}

basic_auth = ('chuhlomin', '')

jira = JIRA(options, basic_auth)

issue = jira.issue('CP-1')
print issue.fields.project.key             # 'JRA'
print issue.fields.issuetype.name          # 'New Feature'
print issue.fields.reporter.displayName    # 'Mike Cannon-Brookes [Atlassian]'