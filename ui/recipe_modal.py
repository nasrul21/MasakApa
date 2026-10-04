"""Recipe details modal and copyable recipe formatting."""

import base64
from html import escape

import streamlit as st
import streamlit.components.v1 as components

from models.meal import Meal
from ui.ingredients import render_ingredient_list
from ui.metadata import render_meal_metadata


def render_copy_button(label: str, recipe_text: str, key: str) -> None:
    """Render a one-click browser clipboard action."""
    encoded_recipe = base64.b64encode(recipe_text.encode("utf-8")).decode(
        "ascii"
    )
    safe_label = escape(label)
    safe_key = escape(key)

    components.html(
        f"""
        <style>
            body {{ margin: 0; background: transparent; }}
            button {{
                width: 100%;
                height: 2.5rem;
                border: 1px solid rgba(128, 128, 128, 0.35);
                border-radius: 10px;
                padding: 0.25rem 0.75rem;
                background: #262730;
                color: #fafafa;
                cursor: pointer;
                font-family: sans-serif;
                font-size: 1rem;
                font-weight: 400;
                line-height: 1.6;
            }}
            button:hover {{
                border-color: #d99100;
                background: #30313d;
            }}
        </style>
        <button id="copy-{safe_key}" type="button">{safe_label}</button>
        <script>
            const button = document.getElementById("copy-{safe_key}");
            const encoded = "{encoded_recipe}";
            button.addEventListener("click", async () => {{
                const bytes = Uint8Array.from(atob(encoded), char =>
                    char.charCodeAt(0)
                );
                const recipe = new TextDecoder().decode(bytes);
                await navigator.clipboard.writeText(recipe);
                button.textContent = "✓ Copied";
                setTimeout(() => {{ button.textContent = "{safe_label}"; }}, 1400);
            }});
        </script>
        """,
        height=45,
    )


def build_recipe_text(
    meal: Meal,
    t: dict[str, str],
) -> str:
    """Build a plain-text representation of a recipe for copying."""
    lines = [
        meal.name,
        (
            f"{meal.duration_minutes} {t['minutes']} · "
            f"{meal.difficulty} · "
            f"{meal.servings} {t['servings']}"
        ),
        "",
        f"{t['why']}:",
        meal.reason,
        "",
        f"{t['ingredients']}:",
    ]

    if meal.available_ingredients:
        lines.append(f"{t['already_have']}:")
        lines.extend(f"- {item}" for item in meal.available_ingredients)

    if meal.missing_ingredients:
        lines.append(f"{t['missing']}:")
        lines.extend(f"- {item}" for item in meal.missing_ingredients)

    if meal.optional_ingredients:
        lines.append(f"{t['optional']}:")
        lines.extend(f"- {item}" for item in meal.optional_ingredients)

    lines.extend(["", f"{t['steps']}:"])
    lines.extend(
        f"{index}. {step}"
        for index, step in enumerate(meal.steps, start=1)
    )

    return "\n".join(lines)


@st.dialog("Recipe")
def render_recipe_modal(
    meal: Meal,
    t: dict[str, str],
) -> None:
    """Render complete recipe details in a modal dialog."""
    st.markdown(f"## {meal.name}")

    render_meal_metadata(meal, t)

    st.markdown('<div class="recipe-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="recipe-section-title"><h3>{t["why"]}</h3></div>',
        unsafe_allow_html=True,
    )
    st.write(meal.reason)

    st.markdown(
        f'<div class="recipe-section-title"><h3>{t["ingredients"]}</h3></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        render_ingredient_list(
            t["already_have"],
            meal.available_ingredients,
            "✓",
        )

    with col2:
        render_ingredient_list(
            t["missing"],
            meal.missing_ingredients,
            "•",
        )

        render_ingredient_list(
            t["optional"],
            meal.optional_ingredients,
            "○",
        )

    st.markdown(
        f'<div class="recipe-section-title"><h3>{t["steps"]}</h3></div>',
        unsafe_allow_html=True,
    )

    for index, step in enumerate(meal.steps, start=1):
        st.markdown(
            f'<div class="recipe-step"><strong>{index}.</strong> '
            f"{escape(step)}</div>",
            unsafe_allow_html=True,
        )

    recipe_text = build_recipe_text(meal, t)
    copy_col, download_col = st.columns(2)

    with copy_col:
        render_copy_button(
            label=t["copy_recipe"],
            recipe_text=recipe_text,
            key=f"copy_recipe_modal_{meal.id}",
        )

    with download_col:
        st.download_button(
            label=t["download_recipe"],
            data=recipe_text,
            file_name=f"{meal.name.lower().replace(' ', '-')}.txt",
            mime="text/plain",
            key=f"download_recipe_modal_{meal.id}",
            use_container_width=True,
        )
