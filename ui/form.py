"""Meal search form component."""

from dataclasses import dataclass

import streamlit as st

from config.moods import MOODS
from state import get_is_generating, get_last_ingredients, get_last_servings


@dataclass(frozen=True)
class MealSearchInputs:
    """Values submitted through the meal search form."""

    ingredients: str
    mood: str
    servings: int
    should_generate: bool


def render_meal_form(
    language: str,
    t: dict[str, str],
) -> MealSearchInputs:
    """Render the meal search form and return its current values."""
    st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)

    ingredients = st.text_area(
        t["ingredients_label"],
        placeholder=t["ingredients_placeholder"],
        help=t["ingredients_help"],
        height=140,
        value=get_last_ingredients(),
    )

    mood = st.pills(
        t["mood_label"],
        MOODS[language],
        default=MOODS[language][0],
    ) or MOODS[language][0]

    servings = st.number_input(
        t["servings_label"],
        min_value=1,
        max_value=12,
        value=get_last_servings(),
        step=1,
    )

    should_generate = st.button(
        f"✨ {t['find_button']}",
        type="primary",
        use_container_width=True,
        disabled=get_is_generating(),
    )

    return MealSearchInputs(
        ingredients=ingredients,
        mood=mood,
        servings=servings,
        should_generate=should_generate,
    )
