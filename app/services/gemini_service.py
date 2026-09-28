import io
import json
import re
from typing import Optional

from PIL import Image

from google import genai
from google.genai import types

from ..config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)


client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def extract_json(text: str):

    text = (text or "").strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:

        raise ValueError(
            "Gemini did not return JSON"
        )

    return json.loads(
        match.group(0)
    )


def create_prompt(
    planner: str,
    payload: dict
):

    return f"""
You are PocketSmart AI,
a practical budget planning assistant.

Planner:
{planner}

User input:

{json.dumps(
    payload,
    indent=2
)}

Return ONLY valid JSON.

Use this structure:

{{
    "summary": "short practical summary",

    "budget_breakdown": [

        {{
            "category": "string",
            "amount": 0,
            "reason": "string"
        }}

    ],

    "recommendations": [

        {{
            "name": "string",
            "category": "string",
            "estimated_price": 0,
            "platform": "Amazon",
            "why": "string",
            "search_hint": "string"
        }}

    ],

    "tips": [
        "string",
        "string",
        "string"
    ]
}}

Rules:

1. Keep spending within the user's budget.

2. Prices are estimates.

3. Do not claim live inventory.

4. Do not claim guaranteed availability.

5. Platforms are search/source suggestions.

6. Generate 5 to 8 useful recommendations.

7. Keep the response practical.

8. Consider the user's preferences.

9. Avoid unnecessary explanations.
"""


def fallback_recommendation(
    planner: str,
    payload: dict
):

    budget = float(
        payload["budget"]
    )

    if planner == "home":

        categories = [

            (
                "Lighting",
                budget * 0.12,
                "Warm LED lighting"
            ),

            (
                "Furniture",
                budget * 0.42,
                "Practical furniture"
            ),

            (
                "Decor",
                budget * 0.18,
                "Wall art and soft decor"
            ),

            (
                "Storage",
                budget * 0.18,
                "Shelves and organizers"
            ),

            (
                "Contingency",
                budget * 0.10,
                "Keep for unexpected costs"
            )
        ]

        recommendations = [

            (
                "LED Ceiling Light",
                "Lighting",
                budget * 0.08,
                "Amazon"
            ),

            (
                "Compact Storage Shelf",
                "Storage",
                budget * 0.15,
                "IKEA"
            ),

            (
                "Accent Chair",
                "Furniture",
                budget * 0.18,
                "Amazon"
            ),

            (
                "Area Rug",
                "Decor",
                budget * 0.10,
                "Flipkart"
            ),

            (
                "Minimal Wall Art Set",
                "Decor",
                budget * 0.06,
                "Amazon"
            )
        ]

    elif planner == "party":

        guests = int(
            payload["guests"]
        )

        categories = [

            (
                "Food & Catering",
                budget * 0.45,
                f"Food for about {guests} guests"
            ),

            (
                "Decoration",
                budget * 0.18,
                "Theme-based decoration"
            ),

            (
                "Venue",
                budget * 0.22,
                "Compare local venue packages"
            ),

            (
                "Entertainment",
                budget * 0.10,
                "Music or activities"
            ),

            (
                "Buffer",
                budget * 0.05,
                "Emergency margin"
            )
        ]

        recommendations = [

            (
                "Catering Package",
                "Food",
                budget * 0.45,
                "Swiggy"
            ),

            (
                "Theme Decoration",
                "Decoration",
                budget * 0.18,
                "Local"
            ),

            (
                "Venue Package",
                "Venue",
                budget * 0.22,
                "OYO"
            ),

            (
                "Cake / Dessert",
                "Food",
                budget * 0.07,
                "Zomato"
            ),

            (
                "Music / Activity Setup",
                "Entertainment",
                budget * 0.08,
                "Local"
            )
        ]

    else:

        categories = [

            (
                "Main Jewelry",
                budget * 0.55,
                "Primary statement piece"
            ),

            (
                "Secondary Piece",
                budget * 0.20,
                "Optional matching piece"
            ),

            (
                "Accessories",
                budget * 0.15,
                "Small coordinating accessory"
            ),

            (
                "Buffer",
                budget * 0.10,
                "Keep room for price differences"
            )
        ]

        recommendations = [

            (
                "Minimal Pendant Necklace",
                "Necklace",
                budget * 0.28,
                "Amazon"
            ),

            (
                "Matching Earrings",
                "Earrings",
                budget * 0.22,
                "Flipkart"
            ),

            (
                "Delicate Bracelet",
                "Bracelet",
                budget * 0.15,
                "Amazon"
            ),

            (
                "Stud Earrings",
                "Earrings",
                budget * 0.12,
                "Flipkart"
            ),

            (
                "Simple Ring",
                "Ring",
                budget * 0.08,
                "Amazon"
            )
        ]

    return {

        "mode": "demo",

        "summary":
            f"Demo-mode plan for a "
            f"{planner} budget of "
            f"₹{budget:,.0f}.",

        "budget_breakdown": [

            {
                "category": category,
                "amount": round(
                    amount,
                    2
                ),
                "reason": reason
            }

            for category,
            amount,
            reason in categories
        ],

        "recommendations": [

            {
                "name": name,
                "category": category,
                "estimated_price": round(
                    price,
                    2
                ),
                "platform": platform,
                "why":
                    "Budget-friendly starting "
                    "option suitable for comparison.",
                "search_hint": name
            }

            for name,
            category,
            price,
            platform
            in recommendations
        ],

        "tips": [

            "Compare at least two options.",

            "Treat prices as estimates.",

            "Keep a small contingency amount."

        ]
    }


async def generate_recommendation(
    planner: str,
    payload: dict,
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None
):

    if not client:

        return fallback_recommendation(
            planner,
            payload
        )

    contents = [

        create_prompt(
            planner,
            payload
        )
    ]

    if image_bytes and mime_type:

        try:

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            contents.append(image)

            contents[0] += """

The attached outfit image is
reference material.

Consider:

- dominant colors
- pattern
- formality
- general style

Do not identify the person.
"""

        except Exception:

            pass

    try:

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=contents,

            config=types.GenerateContentConfig(

                temperature=0.4,

                max_output_tokens=4096,

                response_mime_type="application/json"
            )
        )

        result = extract_json(
            response.text
        )

        result["mode"] = "gemini"

        result["model"] = GEMINI_MODEL

        return result

    except Exception as error:

        result = fallback_recommendation(
            planner,
            payload
        )

        result["mode"] = "fallback"

        result["warning"] = (
            "Gemini request failed. "
            "Demo recommendations were returned."
        )

        return result