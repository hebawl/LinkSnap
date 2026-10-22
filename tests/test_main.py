
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app, generate_short_code


client = TestClient(app)


def test_short_code_has_six_characters():
    code = generate_short_code()

    assert len(code) == 6


def test_short_code_uses_letters_and_digits():
    code = generate_short_code()
    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )

    assert all(character in allowed for character in code)


def test_short_codes_are_randomized():
    codes = {generate_short_code() for _ in range(100)}

    assert len(codes) > 1


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_homepage_loads():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_create_link():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (123,)

    with patch("app.main.get_connection", return_value=mock_conn):
        response = client.post(
            "/links",
            json={"url": "https://example.com"},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 123
    assert len(data["short_code"]) == 6
    assert data["original_url"] == "https://example.com/"
    assert data["short_url"].endswith("/" + data["short_code"])


def test_redirect_to_original_url():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ("https://example.com/",)

    with patch("app.main.get_connection", return_value=mock_conn):
        response = client.get(
            "/abc123",
            follow_redirects=False,
        )

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/"
