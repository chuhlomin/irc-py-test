from abc import ABCMeta


class CommandAbstract:
    __metaclass__ = ABCMeta

    def process_commands(self, command):
        raise NotImplementedError

    def help_list(self):
        return 1
        # raise NotImplementedError
