from abc import ABC, abstractmethod


class HOTPGeneratorPort(ABC):
    @abstractmethod
    def generate_uri(self, session_id: str) -> str:
        pass

    @abstractmethod
    def verify(self, code: str, moving_factor: int = 0) -> bool:
        pass
