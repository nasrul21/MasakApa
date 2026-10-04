"""AI meal-generation provider."""

import json
import re
from dataclasses import replace
from typing import Any

from config.settings import client, settings
from errors import AIConfigurationError, AIRequestError, AIResponseError
from models.meal import Meal


SEASONING_MARKERS = (
    "salt",
    "garam",
    "pepper",
    "lada",
    "sugar",
    "gula",
    "oil",
    "minyak",
    "chili",
    "cabai",
    "cabe",
    "sauce",
    "saus",
    "soy",
    "kecap",
    "spice",
    "rempah",
    "seasoning",
    "bumbu",
)


def _ingredient_is_in_steps(ingredient: str, steps: list[str]) -> bool:
    """Check whether a meaningful ingredient word appears in the steps."""
    ingredient_words = set(re.findall(r"[a-zA-ZÀ-ÿ]+", ingredient.lower()))
    step_words = set(
        re.findall(r"[a-zA-ZÀ-ÿ]+", " ".join(steps).lower())
    )
    return bool(ingredient_words & step_words)


def ensure_missing_seasonings_in_steps(
    meals: list[Meal],
    language: str,
) -> list[Meal]:
    """Add an explicit step for required seasonings omitted by the model."""
    normalized_meals = []

    for meal in meals:
        missing_seasonings = [
            ingredient
            for ingredient in meal.missing_ingredients
            if any(
                marker in ingredient.lower()
                for marker in SEASONING_MARKERS
            )
            and not _ingredient_is_in_steps(ingredient, meal.steps)
        ]

        if not missing_seasonings:
            normalized_meals.append(meal)
            continue

        seasoning_text = ", ".join(missing_seasonings)
        if language == "id":
            seasoning_step = f"Bumbui dengan {seasoning_text} secukupnya."
        else:
            seasoning_step = f"Season with {seasoning_text} to taste."

        normalized_meals.append(
            replace(meal, steps=[*meal.steps, seasoning_step])
        )

    return normalized_meals


def build_system_prompt(language: str) -> str:
    output_language = "English" if language == "en" else "Indonesian"
    difficulty_example = "Easy" if language == "en" else "Mudah"

    return f"""
You are MasakApa, a practical home-cooking assistant.

Your purpose is to help people decide what to cook using ingredients
they already have at home.

The user may describe ingredients informally, approximately, or with
incomplete quantities.

Always respond in {output_language}.

Priorities:
1. Prefer ingredients the user already has.
2. Suggest practical home-cooked meals.
3. Minimize additional ingredients.
4. Respect the user's cooking mood.
5. Respect the requested number of servings.
6. Keep recipes simple and realistic.
7. Prefer familiar everyday meals.
8. Do not invent that the user already owns an ingredient.
9. Clearly separate available ingredients from missing ingredients.
10. Missing ingredients should be limited to reasonable basics.
11. Give exactly 3 different meal ideas.
12. Avoid overly complicated recipes.
13. When mood is "I'm tired" or "Lagi capek", strongly prefer:
    - fewer steps
    - fewer ingredients
    - one pan or one pot
    - minimal preparation
    - shorter cooking time

Writing style:
14. Use a friendly, natural tone suitable for everyday home cooking.
15. Use familiar dish names that people would recognize immediately.
16. Keep the explanation short, practical, and specific to the ingredients.
17. Avoid generic health or nutrition claims unless the user asks for them.
18. Use short, direct cooking instructions with common everyday wording.
19. Avoid unnecessarily formal phrases and unusual or invented words.
20. Never use a strange word in a recipe name when a familiar name is
    available.
21. When responding in Indonesian, use natural Indonesian cooking terms.
22. When responding in Indonesian, use "Mudah", "Sedang", or "Sulit"
    for difficulty.

Seasoning rules:
23. Treat salt, sugar, cooking oil, pepper, chili, sauces, and spices as
    unavailable unless the user explicitly provides them.
24. If a recipe requires a seasoning that was not provided, list it in
    missing_ingredients and use it in the cooking steps.
25. Keep missing seasonings limited to the essential amount needed for the
    recipe.
26. Put optional seasonings such as chili or garnish in optional_ingredients
    when the recipe can work without them.

Return JSON only.

The JSON must use exactly this structure:

{{
  "meals": [
    {{
      "id": "meal-1",
      "name": "Meal name",
      "duration_minutes": 25,
      "difficulty": "{difficulty_example}",
      "reason": "Short explanation why this meal fits the user.",
      "available_ingredients": [
        "ingredient 1",
        "ingredient 2"
      ],
      "missing_ingredients": [
        "ingredient 1"
      ],
      "optional_ingredients": [
        "ingredient 1"
      ],
      "servings": 4,
      "steps": [
        "Step one",
        "Step two",
        "Step three"
      ]
    }}
  ]
}}

Rules:
- Return exactly 3 meals.
- steps should contain around 4-7 concise steps.
- duration_minutes must be an integer.
- available_ingredients must only contain ingredients inferred from
  the user's input.
- missing_ingredients should contain ingredients required to make the
  recipe work.
- optional_ingredients should genuinely be optional.
- Do not wrap JSON in markdown code fences.
""".strip()


def build_user_prompt(
    ingredients: str,
    mood: str,
    servings: int,
    generation_number: int,
) -> str:
    retry_instruction = ""

    if generation_number > 0:
        retry_instruction = """
The user requested different ideas.
Avoid repeating the most obvious previous suggestions where possible.
"""

    return f"""
Ingredients available:

{ingredients}

Cooking mood:
{mood}

Servings:
{servings}

{retry_instruction}

Generate exactly 3 realistic meal ideas.
""".strip()


def clean_json_response(content: str) -> str:
    content = re.sub(
        r"<think>.*?</think>",
        "",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    ).strip()

    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    # Small local models sometimes add a short explanation before or after
    # an otherwise valid JSON object. Keep only the JSON payload.
    start = content.find("{")
    end = content.rfind("}")

    if start >= 0 and end > start:
        return content[start : end + 1]

    return content


def generate_meal_ideas(
    ingredients: str,
    mood: str,
    servings: int,
    language: str,
    generation_number: int,
) -> list[Meal]:
    """Generate and normalize meal ideas from the configured AI provider."""
    if not settings.ai_model:
        raise AIConfigurationError("AI_MODEL is not configured.")

    try:
        response = client.chat.completions.create(
            model=settings.ai_model,
            temperature=0.6,
            messages=[
                {
                    "role": "system",
                    "content": build_system_prompt(language),
                },
                {
                    "role": "user",
                    "content": build_user_prompt(
                        ingredients=ingredients,
                        mood=mood,
                        servings=servings,
                        generation_number=generation_number,
                    ),
                },
            ],
        )
    except Exception as error:
        raise AIRequestError("AI request failed.") from error

    content = response.choices[0].message.content

    if not content:
        raise AIResponseError("AI returned an empty response.")

    try:
        parsed: dict[str, Any] = json.loads(clean_json_response(content))
    except (json.JSONDecodeError, TypeError) as error:
        raise AIResponseError("AI returned invalid JSON.") from error

    if not isinstance(parsed, dict):
        raise AIResponseError("AI response must be a JSON object.")

    raw_meals = parsed.get("meals", [])

    if not isinstance(raw_meals, list) or not raw_meals:
        raise AIResponseError("AI returned no meals.")

    try:
        meals = [
            Meal.from_dict(meal, index)
            for index, meal in enumerate(raw_meals[:3])
        ]
        return ensure_missing_seasonings_in_steps(meals, language)
    except (TypeError, ValueError) as error:
        raise AIResponseError("AI returned invalid meal data.") from error
