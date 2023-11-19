import abc


class Command(abc.ABC):
    @abc.abstractmethod
    def do(self, editor):
        ...

    @abc.abstractmethod
    def undo(self, editor):
        ...
