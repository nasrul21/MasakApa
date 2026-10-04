"""Meal metadata badge component."""

from html import escape

import streamlit as st

from models.meal import Meal


def render_meal_metadata(
    meal: Meal,
    t: dict[str, str],
) -> None:
    """Render compact visual badges for meal metadata."""
    difficulty = escape(meal.difficulty)

    st.markdown(
        f"""
        <div class="meal-badges">
            <span class="meal-badge meal-badge-time">
                ⏱ {meal.duration_minutes} {t['minutes']}
            </span>
            <span class="meal-badge meal-badge-difficulty">
                ◆ {difficulty}
            </span>
            <span class="meal-badge meal-badge-servings">
                ♟ {meal.servings} {t['servings']}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
