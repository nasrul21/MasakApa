"""Ingredient list rendering helpers."""

import streamlit as st


def render_ingredient_list(
    title: str,
    items: list[str],
    symbol: str,
) -> None:
    """Render a titled list of ingredients when items are available."""
    if not items:
        return

    st.markdown(f"**{title}**")

    for item in items:
        st.markdown(f"{symbol} {item}")
