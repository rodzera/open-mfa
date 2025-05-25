from abc import ABC, abstractmethod


class OTPGeneratorPort(ABC):
    @abstractmethod
    def generate_code(self, moving_factor: int) -> str:
        pass
