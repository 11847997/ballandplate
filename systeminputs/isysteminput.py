import abc

from models import request


class ISystemInput(abc.ABC):

    @abc.abstractmethod
    def execute(self, request_model: request.Request):
        pass