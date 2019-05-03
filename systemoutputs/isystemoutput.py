import abc

from models import response


class ISystemOutput(abc.ABC):
    @abc.abstractmethod
    def present(self, reponse_model: response.Response):
        pass
