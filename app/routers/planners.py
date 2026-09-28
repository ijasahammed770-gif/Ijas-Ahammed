from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException
)

from ..auth import current_user

from ..models import (
    HomeRequest,
    PartyRequest
)

from ..services.gemini_service import (
    generate_recommendation
)

from ..services.history_service import (
    save_recommendation
)


router = APIRouter()


async def save_result(
    user,
    planner,
    budget,
    payload,
    result
):

    save_recommendation(
        user["id"],
        planner,
        budget,
        payload,
        result
    )

    return result


@router.post("/generate-home")
async def generate_home(
    data: HomeRequest,
    user=Depends(current_user)
):

    payload = data.model_dump()

    result = await generate_recommendation(
        "home",
        payload
    )

    return await save_result(
        user,
        "home",
        data.budget,
        payload,
        result
    )


@router.post("/generate-party")
async def generate_party(
    data: PartyRequest,
    user=Depends(current_user)
):

    payload = data.model_dump()

    result = await generate_recommendation(
        "party",
        payload
    )

    return await save_result(
        user,
        "party",
        data.budget,
        payload,
        result
    )


@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: float,

    occasion: str,

    style: str = "Elegant",

    outfit_color: str = "",

    notes: str = "",

    outfit_image: UploadFile | None = File(
        default=None
    ),

    user=Depends(current_user)
):

    if budget <= 0:

        raise HTTPException(
            400,
            "Budget must be positive"
        )

    if len(occasion.strip()) < 2:

        raise HTTPException(
            400,
            "Occasion is required"
        )

    image_bytes = None

    mime_type = None

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                400,
                "Use JPG, PNG or WEBP image"
            )

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > (
            5 * 1024 * 1024
        ):

            raise HTTPException(
                400,
                "Image must be 5 MB or smaller"
            )

        mime_type = (
            outfit_image.content_type
        )

    payload = {

        "budget": budget,

        "occasion":
            occasion.strip(),

        "style":
            style.strip(),

        "outfit_color":
            outfit_color.strip(),

        "notes":
            notes.strip()
    }

    result = await generate_recommendation(

        "jewelry",

        payload,

        image_bytes,

        mime_type
    )

    return await save_result(

        user,

        "jewelry",

        budget,

        payload,

        result
    )