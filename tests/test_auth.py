from unittest.mock import MagicMock, patch

from src.auth import (
    get_user_info,
    sign_in_with_email_password,
    sign_in_with_google_id_token,
    sign_up_with_email_password,
)


@patch("src.auth.requests.post")
@patch("src.auth.FIREBASE_API_KEY", "test-key")
def test_sign_in_with_email_password_success(mock_post):
    response = MagicMock()
    response.json.return_value = {"idToken": "token", "email": "user@example.com", "localId": "abc"}
    mock_post.return_value = response

    result = sign_in_with_email_password("user@example.com", "pw")
    assert result["token"] == "token"


@patch("src.auth.requests.post")
@patch("src.auth.FIREBASE_API_KEY", "test-key")
def test_get_user_info_success(mock_post):
    response = MagicMock()
    response.json.return_value = {"users": [{"email": "user@example.com", "localId": "abc"}]}
    mock_post.return_value = response

    result = get_user_info("token")
    assert result["email"] == "user@example.com"


@patch("src.auth.requests.post")
@patch("src.auth.FIREBASE_API_KEY", "test-key")
def test_sign_up_with_email_password_success(mock_post):
    response = MagicMock()
    response.json.return_value = {
        "idToken": "token",
        "email": "user@example.com",
        "localId": "abc",
    }
    mock_post.return_value = response

    result = sign_up_with_email_password("user@example.com", "pw")
    assert result["token"] == "token"
    assert result["email"] == "user@example.com"


@patch("src.auth.get_user_info")
def test_sign_in_with_google_id_token(mock_get_user_info):
    mock_get_user_info.return_value = {"email": "user@example.com", "localId": "abc"}
    result = sign_in_with_google_id_token("token")
    assert result["provider"] == "google"
