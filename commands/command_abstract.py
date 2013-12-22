from abc import ABCMeta


class CommandAbstract:
    __metaclass__ = ABCMeta

    def process_commands(self, command):
        raise NotImplementedError