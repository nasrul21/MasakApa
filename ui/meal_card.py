"""Meal summary card component."""

import streamlit as st

from models.meal import Meal
from ui.ingredients import render_ingredient_list
from ui.metadata import render_meal_metadata
from ui.recipe_modal import render_recipe_modal


def render_meal_card(
    meal: Meal,
    index: int,
    t: dict[str, str],
    best_match: bool = False,
) -> None:
    """Render a meal summary and its recipe action."""
    with st.container(border=True):
        title_col, badge_col = st.columns([4, 1])

        with title_col:
            st.markdown(f"### {meal.name}")

        with badge_col:
            if best_match:
                st.markdown(
                    f'<div class="best-match">★ {t["best_match"]}</div>',
                    unsafe_allow_html=True,
                )

        render_meal_metadata(meal, t)

        st.write(meal.reason)

        available_count = len(meal.available_ingredients)

        if available_count:
            st.caption(f"✓ {available_count} {t['available_count']}")

            with st.expander(
                f"✓ {t['already_have']} ({available_count})",
                expanded=False,
            ):
                render_ingredient_list(
                    t["already_have"],
                    meal.available_ingredients,
                    "✓",
                )

        if meal.missing_ingredients:
            missing_count = len(meal.missing_ingredients)

            with st.expander(
                f"＋ {t['missing']} ({missing_count})",
                expanded=False,
            ):
                render_ingredient_list(
                    t["missing"],
                    meal.missing_ingredients,
                    "•",
                )

        if meal.optional_ingredients:
            optional_count = len(meal.optional_ingredients)

            with st.expander(
                f"○ {t['optional']} ({optional_count})",
                expanded=False,
            ):
                render_ingredient_list(
                    t["optional"],
                    meal.optional_ingredients,
                    "○",
                )

        if st.button(
            t["view_recipe"],
            key=f"view_recipe_{index}",
            use_container_width=True,
        ):
            render_recipe_modal(meal, t)
