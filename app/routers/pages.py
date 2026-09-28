from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import current_user
from app.services.history_service import get_history


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# =========================
# HOME
# =========================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================
# LOGIN PAGE
# =========================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


# =========================
# REGISTER PAGE
# =========================

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )


# =========================
# DASHBOARD
# =========================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    user = await current_user(request)

    # User is not logged in
    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    history = get_history(user["id"])

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
            "history": history
        }
    )


# =========================
# HISTORY
# =========================

@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):

    user = await current_user(request)

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    history = get_history(user["id"])

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": user,
            "history": history
        }
    )


# =========================
# HOME PLANNER
# =========================

@router.get("/home-planner", response_class=HTMLResponse)
async def home_planner(request: Request):

    user = await current_user(request)

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request,
            "user": user
        }
    )


# =========================
# PARTY PLANNER
# =========================

@router.get("/party-planner", response_class=HTMLResponse)
async def party_planner(request: Request):

    user = await current_user(request)

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "request": request,
            "user": user
        }
    )


# =========================
# JEWELRY PLANNER
# =========================

@router.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_planner(request: Request):

    user = await current_user(request)

    if not user:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "request": request,
            "user": user
        }
    )