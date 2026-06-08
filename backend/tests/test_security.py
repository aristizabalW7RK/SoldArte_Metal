from backend.core.security import hash_password, verify_password, create_access_token, decode_token


def test_hash_password_returns_string():
    hashed = hash_password("mi_password_segura")
    assert isinstance(hashed, str)
    assert hashed != "mi_password_segura"


def test_verify_password_correct():
    hashed = hash_password("mi_password_segura")
    assert verify_password("mi_password_segura", hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("mi_password_segura")
    assert verify_password("password_incorrecta", hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "1"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token_valid():
    token = create_access_token({"sub": "42"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "42"


def test_decode_token_invalid():
    payload = decode_token("token_invalido")
    assert payload is None


def test_decode_token_expired(monkeypatch):
    from datetime import timedelta

    monkeypatch.setattr("backend.core.security.settings.ACCESS_TOKEN_EXPIRE_MINUTES", -1)
    token = create_access_token({"sub": "1"})
    payload = decode_token(token)
    assert payload is None
