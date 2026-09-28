import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.database import get_user_by_id


# =========================
# PASSWORD HASHING
# =========================

def hash_password(password: str) -> str:
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(
    password: str,
    stored_hash: str
) -> bool:

    try:

        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return secrets.compare_digest(
            actual_hash,
            expected_hash
        )

    except Exception:

        return False


# =========================
# JWT TOKEN
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# GET CURRENT USER
# =========================

def get_current_user_from_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return get_user_by_id(int(user_id))

    except (
        JWTError,
        ValueError,
        TypeError
    ):

        return None


# =========================
# CURRENT USER
# =========================

async def current_user(
    request
):

    token = request.cookies.get(
        "access_token"
    )

    if not token:
        return None

    return get_current_user_from_token(
        token
    )