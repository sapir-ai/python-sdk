from abc import abstractmethod, ABCMeta
from typing import Any, Mapping, BinaryIO


class InferenceManager(metaclass=ABCMeta):
    @abstractmethod
    def load_state_dict(self, state_dict: Mapping[str, Any]) -> None:
        pass

    @abstractmethod
    def handle(self, w: BinaryIO, r: BinaryIO) -> str:
        """handles requests and returns the content type"""
        pass
