"""Application footer component."""

import streamlit as st


def render_footer(
    ai_model: str,
    t: dict[str, str],
) -> None:
    """Render model information at the bottom of the application."""
    st.divider()

    if ai_model:
        st.caption(
            f"✨ Open-weight AI · "
            f"{t['model_label']}: {ai_model}"
        )
    else:
        st.caption("✨ Open-weight AI · Model not configured")
