"""Shared Streamlit styling."""

import streamlit as st


def render_styles() -> None:
    """Inject the application's shared CSS styles."""
    st.markdown(
        """
        <style>
            #MainMenu {
                visibility: hidden;
            }

            header[data-testid="stHeader"] {
                display: none;
            }

            footer {
                visibility: hidden;
            }

            .block-container {
                max-width: 768px;
                padding-top: 1rem;
                padding-bottom: 4rem;
            }

            .form-divider {
                border-top: 1px solid rgba(128, 128, 128, 0.3);
                margin: 0.25rem 0 1rem;
            }

            .app-brand {
                font-size: 2.2rem;
                font-weight: 800;
                margin-bottom: 0;
            }

            .app-subtitle {
                font-size: 1.4rem;
                color: #666;
                margin-top: -5px;
                margin-bottom: 4px;
            }

            .meal-meta {
                color: #666;
                font-size: 0.9rem;
            }

            .meal-reason {
                margin-top: 0.75rem;
                margin-bottom: 1rem;
            }

            .meal-badges {
                display: flex;
                flex-wrap: wrap;
                gap: 0.4rem;
                margin: 0.35rem 0 0.85rem;
            }

            .meal-badge {
                border: 1px solid rgba(128, 128, 128, 0.35);
                border-radius: 999px;
                font-size: 0.8rem;
                padding: 0.2rem 0.6rem;
            }

            .meal-badge-time {
                background: rgba(124, 179, 66, 0.14);
            }

            .meal-badge-difficulty {
                background: rgba(245, 169, 0, 0.16);
            }

            .meal-badge-servings {
                background: rgba(233, 196, 106, 0.14);
            }

            .best-match {
                background: rgba(255, 193, 7, 0.12);
                border: 1px solid rgba(255, 211, 105, 0.35);
                border-radius: 999px;
                color: #f6d37a;
                font-size: 0.85rem;
                font-weight: 700;
                padding: 0.25rem 0.45rem;
                text-align: center;
            }

            @media (prefers-color-scheme: light) {
                .best-match {
                    background: rgba(255, 224, 130, 0.32);
                    border-color: rgba(255, 193, 7, 0.35);
                    color: #8a6500;
                }
            }

            .recipe-section-title {
                border-bottom: 1px solid rgba(128, 128, 128, 0.25);
                margin-top: 1.25rem;
                padding-bottom: 0.35rem;
            }

            .recipe-divider {
                height: 1px;
                margin: 0.5rem 0 0.85rem;
                background: linear-gradient(
                    90deg,
                    #d99100 0%,
                    rgba(217, 145, 0, 0.35) 35%,
                    rgba(128, 128, 128, 0.18) 72%,
                    transparent 100%
                );
            }

            .recipe-step {
                border-left: 3px solid #f5a900;
                margin: 0.5rem 0;
                padding: 0.55rem 0.75rem;
            }

            .recipe-copy-hint {
                color: #666;
                font-size: 0.85rem;
                margin-bottom: 0.35rem;
            }


            .ingredient-ok {
                margin-bottom: 3px;
            }

            .ingredient-missing {
                margin-bottom: 3px;
            }

            div[data-testid="stButton"] > button {
                border-radius: 10px;
            }

            div[data-testid="stTextArea"] textarea {
                border-radius: 12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
