"""Centralized Streamlit session-state access."""

from typing import Optional

import streamlit as st

from models.meal import Meal


def initialize_state() -> None:
    """Initialize application session state with safe defaults."""
    defaults = {
        "meals": [],
        "last_ingredients": "",
        "last_mood": "",
        "last_servings": 4,
        "generation_number": 0,
        "is_generating": False,
        "pending_generation": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_meals() -> list[Meal]:
    """Return the currently generated meal ideas."""
    return st.session_state.meals


def get_last_ingredients() -> str:
    """Return the ingredients used for the latest generation."""
    return st.session_state.last_ingredients


def get_last_mood() -> str:
    """Return the mood used for the latest generation."""
    return st.session_state.last_mood


def get_last_servings() -> int:
    """Return the servings used for the latest generation."""
    return st.session_state.last_servings


def get_generation_number() -> int:
    """Return the current generation number."""
    return st.session_state.generation_number


def reset_generation_number() -> None:
    """Reset the generation number for a new search."""
    st.session_state.generation_number = 0


def increment_generation_number() -> int:
    """Increment and return the generation number for a retry."""
    st.session_state.generation_number += 1
    return st.session_state.generation_number


def save_generation(
    meals: list[Meal],
    ingredients: str,
    mood: str,
    servings: int,
) -> None:
    """Store generated meals and the inputs that produced them."""
    st.session_state.meals = meals
    st.session_state.last_ingredients = ingredients
    st.session_state.last_mood = mood
    st.session_state.last_servings = servings


def clear_results() -> None:
    """Remove generated meals while keeping the last search inputs."""
    st.session_state.meals = []


def get_is_generating() -> bool:
    """Return whether an AI generation is currently running."""
    return st.session_state.is_generating


def set_is_generating(value: bool) -> None:
    """Set the AI generation status."""
    st.session_state.is_generating = value


def request_generation(retry: bool = False) -> None:
    """Queue a generation and mark its controls as busy."""
    st.session_state.pending_generation = "retry" if retry else "new"
    st.session_state.is_generating = True


def get_pending_generation() -> Optional[str]:
    """Return the queued generation type, if one exists."""
    return st.session_state.pending_generation


def clear_pending_generation() -> None:
    """Clear the queued generation request."""
    st.session_state.pending_generation = None

