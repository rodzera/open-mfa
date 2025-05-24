from abc import ABC, abstractmethod


class TOTPGeneratorPort(ABC):
    @abstractmethod
    def generate_uri(self, session_id: str) -> str:
        pass

    @abstractmethod
    def verify(self, code: str) -> bool:
        pass
