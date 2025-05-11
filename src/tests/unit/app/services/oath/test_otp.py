from src.app.services.oath import OTPService
from src.app.repositories.oath import OATHRepository


def test_service_type_attr() -> None:
    assert OTPService.service_type == "otp"

def test_repository_class_attr() -> None:
    assert OTPService.repo == OATHRepository
