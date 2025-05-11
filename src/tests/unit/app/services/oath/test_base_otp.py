from abc import ABC

from src.app.services.oath import OATHService


def test_is_abc_sub_class() -> None:
    assert issubclass(OATHService, ABC)

def test_has_abstract_methods() -> None:
    abstract_methods = OATHService.__abstractmethods__
    assert "create" in abstract_methods
    assert "verify" in abstract_methods
