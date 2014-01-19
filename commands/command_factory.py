from commands.jira_command import JiraCommand


class CommandFactory(object):

    @staticmethod
    def get_command(name):
        objects = {
           'jira': JiraCommand,
            #'jenkins': JenkinsCommand,
            #'vote': VoteCommand,
        }

        if name not in objects.keys():
            return None

        return objects[name]()