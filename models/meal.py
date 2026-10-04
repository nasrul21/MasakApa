"""Typed meal model and AI response normalization."""

from dataclasses import dataclass
from typing import Any, Mapping


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    return [str(item) for item in value]


@dataclass(frozen=True)
class Meal:
    """A generated meal idea and its cooking instructions."""

    id: str
    name: str
    duration_minutes: int
    difficulty: str
    reason: str
    available_ingredients: list[str]
    missing_ingredients: list[str]
    optional_ingredients: list[str]
    servings: int
    steps: list[str]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], index: int) -> "Meal":
        """Create a meal from one AI response item."""
        return cls(
            id=str(data.get("id", f"meal-{index + 1}")),
            name=str(data.get("name", "Untitled meal")),
            duration_minutes=int(data.get("duration_minutes", 0)),
            difficulty=str(data.get("difficulty", "Easy")),
            reason=str(data.get("reason", "")),
            available_ingredients=_string_list(
                data.get("available_ingredients", [])
            ),
            missing_ingredients=_string_list(
                data.get("missing_ingredients", [])
            ),
            optional_ingredients=_string_list(
                data.get("optional_ingredients", [])
            ),
            servings=int(data.get("servings", 1)),
            steps=_string_list(data.get("steps", [])),
        )
