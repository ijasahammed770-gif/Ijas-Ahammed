from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

from app.database import (
    get_user_by_email,
    create_user
)


router = APIRouter()


# =========================
# REGISTER
# =========================

@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    # Remove unnecessary spaces
    name = name.strip()
    email = email.strip().lower()

    # Check if email already exists
    existing_user = get_user_by_email(email)

    if existing_user:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Email already registered."
            }
        )

    # Create password hash
    password_hash = hash_password(password)

    # Create user
    create_user(
        name=name,
        email=email,
        password_hash=password_hash
    )

    return {
        "message": "Registration successful!"
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):

    email = email.strip().lower()

    # Find user
    user = get_user_by_email(email)

    if not user:

        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid email or password."
            }
        )

    # Check password
    if not verify_password(
        password,
        user["password_hash"]
    ):

        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid email or password."
            }
        )

    # Create JWT token
    token = create_access_token(
        {
            "sub": str(user["id"])
        }
    )

    response = JSONResponse(
        content={
            "message": "Login successful!"
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return response


# =========================
# LOGOUT
# =========================

@router.post("/logout")
async def logout():

    response = JSONResponse(
        content={
            "message": "Logged out successfully."
        }
    )

    response.delete_cookie("access_token")

    return response