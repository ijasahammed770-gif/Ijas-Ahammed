from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    username: EmailStr

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    rooms: list[str] = Field(
        min_length=1
    )

    style: str = Field(
        default="Modern",
        max_length=50
    )

    items: dict[str, int] = {}


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10_000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="Flexible",
        max_length=100
    )

    city: str = Field(
        default="Local",
        max_length=100
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=100
    )

    style: str = Field(
        default="Elegant",
        max_length=80
    )

    outfit_color: Optional[str] = Field(
        default=None,
        max_length=80
    )

    notes: Optional[str] = Field(
        default="",
        max_length=500
    )

    @field_validator("budget")
    @classmethod
    def budget_positive(cls, value):

        if value <= 0:
            raise ValueError(
                "Budget must be positive"
            )

        return value