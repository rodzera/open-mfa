from src.app.services.oath import HOTPService
from src.app.repositories.oath import OTPRepository


def test_service_type_attr() -> None:
    assert HOTPService.service_type == "hotp"

def test_repository_class_attr() -> None:
    assert HOTPService.repo == OTPRepository
