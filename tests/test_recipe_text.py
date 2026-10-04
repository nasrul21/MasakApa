import unittest

from models.meal import Meal
from ui.recipe_modal import build_recipe_text


ENGLISH_LABELS = {
    "minutes": "min",
    "servings": "servings",
    "why": "Why this works",
    "ingredients": "Ingredients",
    "steps": "How to cook",
    "already_have": "You already have",
    "missing": "You may need",
    "optional": "Optional",
}


class RecipeTextTests(unittest.TestCase):
    def test_recipe_text_contains_details_and_numbered_steps(self):
        meal = Meal.from_dict(
            {
                "name": "Egg noodles",
                "duration_minutes": 15,
                "servings": 2,
                "reason": "Quick dinner",
                "available_ingredients": ["eggs"],
                "missing_ingredients": ["noodles"],
                "steps": ["Boil noodles", "Add eggs"],
            },
            0,
        )

        text = build_recipe_text(meal, ENGLISH_LABELS)

        self.assertIn("Egg noodles", text)
        self.assertIn("- eggs", text)
        self.assertIn("- noodles", text)
        self.assertIn("1. Boil noodles", text)
        self.assertIn("2. Add eggs", text)

    def test_empty_optional_section_is_omitted(self):
        meal = Meal.from_dict({"steps": ["Cook"]}, 0)

        text = build_recipe_text(meal, ENGLISH_LABELS)

        self.assertNotIn("Optional:", text)


if __name__ == "__main__":
    unittest.main()
