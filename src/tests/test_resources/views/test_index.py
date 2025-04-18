from flask.testing import FlaskClient


def test_redirect_302(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/apidocs/"
