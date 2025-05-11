from src.app.services.oath import TOTPService
from src.app.repositories.oath import OATHRepository

def test_service_type_attr() -> None:
    assert TOTPService.service_type == "totp"

def test_repository_class_attr() -> None:
    assert TOTPService.repo == OATHRepository
