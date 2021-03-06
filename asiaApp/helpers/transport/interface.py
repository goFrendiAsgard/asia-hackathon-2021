from typing import Any, Callable
import abc

class RPC(abc.ABC):

    @abc.abstractmethod
    def handle(self, rpc_name: str) -> Callable[..., Any]:
        pass

    @abc.abstractmethod
    def call(self, rpc_name: str, *args: Any) -> Any:
        pass

    @abc.abstractmethod
    def shutdown(self) -> Any:
        pass


class MessageBus(abc.ABC):

    @abc.abstractmethod
    def handle(self, event_name: str) -> Callable[..., Any]:
        pass

    @abc.abstractmethod
    def publish(self, event_name: str, message: Any) -> Any:
        pass

    @abc.abstractmethod
    def shutdown(self) -> Any:
        pass