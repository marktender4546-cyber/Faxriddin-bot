"""Small standard-library checks for Telegram initData validation."""
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

from app import validate_telegram_init_data


def make_init_data(token: str, user: dict, auth_date: int | None = None) -> str:
    values = {
        "auth_date": str(auth_date if auth_date is not None else int(time.time())),
        "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
        "user": json.dumps(user, separators=(",", ":")),
        "signature": "demo-ed25519-signature",
    }
    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(values.items()))
    secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    values["hash"] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode(values)


def test_valid_init_data() -> None:
    token = "test-bot-token"
    payload = make_init_data(token, {"id": 12345, "first_name": "Demo"})
    user = validate_telegram_init_data(payload, token)
    assert user["id"] == 12345


def test_tampered_init_data_is_rejected() -> None:
    token = "test-bot-token"
    payload = make_init_data(token, {"id": 12345, "first_name": "Demo"})
    try:
        validate_telegram_init_data(payload + "&query_id=changed", token)
    except ValueError:
        return
    raise AssertionError("Tampered initData must be rejected")


def test_stale_init_data_is_rejected() -> None:
    token = "test-bot-token"
    payload = make_init_data(token, {"id": 12345}, int(time.time()) - 90000)
    try:
        validate_telegram_init_data(payload, token)
    except ValueError:
        return
    raise AssertionError("Expired initData must be rejected")


if __name__ == "__main__":
    test_valid_init_data()
    test_tampered_init_data_is_rejected()
    test_stale_init_data_is_rejected()
    print("All initData validation checks passed.")
