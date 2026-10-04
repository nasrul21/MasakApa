"""Generated meal results components."""

import streamlit as st

from models.meal import Meal
from state import get_is_generating
from ui.meal_card import render_meal_card


def meal_match_score(meal: Meal) -> tuple[int, int, int]:
    """Return comparable local scores for selecting the best meal match."""
    return (
        len(meal.available_ingredients),
        -len(meal.missing_ingredients),
        -meal.duration_minutes,
    )


def render_results(
    meals: list[Meal],
    t: dict[str, str],
    last_ingredients: str,
    last_mood: str,
    last_servings: int,
) -> bool:
    """Render generated meals and return whether retry was requested."""
    st.divider()
    st.markdown(f"## {t['results_title']}")

    if last_ingredients:
        st.caption(f"{t['based_on']}: {last_ingredients}")

    if last_mood:
        st.caption(
            f"{t['mood']}: {last_mood} · "
            f"{last_servings} {t['servings']}"
        )

    st.write("")

    best_match_index = max(
        range(len(meals)),
        key=lambda index: meal_match_score(meals[index]),
    )

    for index, meal in enumerate(meals):
        render_meal_card(
            meal=meal,
            index=index,
            t=t,
            best_match=index == best_match_index,
        )

    st.write("")

    return st.button(
        f"↻ {t['try_again']}",
        use_container_width=True,
        disabled=get_is_generating(),
    )
