"""Header and language selector components."""

import streamlit as st

from config.translations import TRANSLATIONS


def render_header() -> tuple[str, dict[str, str]]:
    """Render the app header and return the selected language and labels."""
    header_left, header_right = st.columns([5, 1])

    with header_right:
        language_options = {
            "🇬🇧 EN": "en",
            "🇮🇩 ID": "id",
        }
        selected_language = st.selectbox(
            "Language",
            list(language_options),
            key="language_selector",
            label_visibility="collapsed",
        )
        language = language_options[selected_language]
        st.session_state.language = language

    labels = TRANSLATIONS[language]

    with header_left:
        st.markdown(
            '<div class="app-brand">🍳 MasakApa</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="app-subtitle">{labels["subtitle"]}</div>',
            unsafe_allow_html=True,
        )

    st.write(labels["description"])

    return language, labels
