import json
import logging
import streamlit as st

from config.settings import settings
from errors import AIConfigurationError, AIRequestError, AIResponseError
from providers.ai import generate_meal_ideas
from state import (
    get_generation_number,
    get_pending_generation,
    get_last_ingredients,
    get_last_mood,
    get_last_servings,
    get_meals,
    increment_generation_number,
    initialize_state,
    clear_pending_generation,
    request_generation,
    reset_generation_number,
    save_generation,
    set_is_generating,
)
from ui.header import render_header
from ui.footer import render_footer
from ui.form import MealSearchInputs, render_meal_form
from ui.results import render_results
from ui.styles import render_styles

logger = logging.getLogger(__name__)

# =========================================================
# App configuration
# =========================================================

st.set_page_config(
    page_title="MasakApa",
    page_icon="🍳",
    layout="centered"
)

# Keep the existing local name while the rest of the app is migrated to
# use the Settings object directly in a later refactoring phase.
AI_MODEL = settings.ai_model

render_styles()

initialize_state()

# =========================================================
# Header / language
# =========================================================

language, t = render_header()

# =========================================================
# Main form
# =========================================================

inputs = render_meal_form(language, t)


def generate_and_store_meals(
    inputs: MealSearchInputs,
    language: str,
    t: dict[str, str],
    retry: bool = False,
) -> bool:
    """Generate meals for form inputs and store them in session state."""
    if not inputs.ingredients.strip():
        st.warning(t["empty_ingredients"])
        set_is_generating(False)
        return False

    if not AI_MODEL:
        st.error(t["no_model"])
        set_is_generating(False)
        return False

    set_is_generating(True)

    try:
        with st.spinner(t["loading"]):
            if retry:
                generation_number = increment_generation_number()
            else:
                reset_generation_number()
                generation_number = get_generation_number()

            meals = generate_meal_ideas(
                ingredients=inputs.ingredients,
                mood=inputs.mood,
                servings=inputs.servings,
                language=language,
                generation_number=generation_number,
            )

            save_generation(
                meals=meals,
                ingredients=inputs.ingredients,
                mood=inputs.mood,
                servings=inputs.servings,
            )
            return True

    except AIConfigurationError:
        logger.error("AI model configuration is missing")
        st.error(t["no_model"])
        return False

    except AIResponseError:
        logger.exception("AI returned an invalid meal response")
        st.error(t["invalid_response"])
        return False

    except AIRequestError:
        logger.exception("AI request failed")
        st.error(t["generation_error"])
        return False

    except json.JSONDecodeError:
        logger.exception("Unexpected JSON parsing error")
        st.error(
            f"{t['generation_error']} "
            "The model returned invalid JSON."
        )
        return False

    except Exception as error:
        logger.exception("Unexpected meal generation error: %s", error)
        st.error(t["generation_error"])
        return False

    finally:
        set_is_generating(False)


if inputs.should_generate:
    request_generation()
    st.rerun()


# =========================================================
# Results
# =========================================================

if get_meals():
    if render_results(
        meals=get_meals(),
        t=t,
        last_ingredients=get_last_ingredients(),
        last_mood=get_last_mood(),
        last_servings=get_last_servings(),
    ):
        request_generation(retry=True)
        st.rerun()


pending_generation = get_pending_generation()

if pending_generation:
    clear_pending_generation()

    if pending_generation == "retry":
        pending_inputs = MealSearchInputs(
            ingredients=get_last_ingredients(),
            mood=get_last_mood(),
            servings=get_last_servings(),
            should_generate=True,
        )
    else:
        pending_inputs = inputs

    generation_succeeded = generate_and_store_meals(
        pending_inputs,
        language,
        t,
        retry=pending_generation == "retry",
    )

    if generation_succeeded:
        st.rerun()


render_footer(AI_MODEL, t)
