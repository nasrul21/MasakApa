import unittest

from models.meal import Meal


class MealValidationTests(unittest.TestCase):
    def test_missing_fields_use_defaults(self):
        meal = Meal.from_dict({}, 0)

        self.assertEqual(meal.id, "meal-1")
        self.assertEqual(meal.name, "Untitled meal")
        self.assertEqual(meal.duration_minutes, 0)
        self.assertEqual(meal.servings, 1)
        self.assertEqual(meal.available_ingredients, [])
        self.assertEqual(meal.steps, [])

    def test_fields_are_normalized_to_expected_types(self):
        meal = Meal.from_dict(
            {
                "duration_minutes": "25",
                "servings": "2",
                "available_ingredients": ["eggs", 3],
                "steps": ["Mix", 4],
            },
            1,
        )

        self.assertEqual(meal.duration_minutes, 25)
        self.assertEqual(meal.servings, 2)
        self.assertEqual(meal.available_ingredients, ["eggs", "3"])
        self.assertEqual(meal.steps, ["Mix", "4"])

    def test_non_list_ingredients_and_steps_become_empty(self):
        meal = Meal.from_dict(
            {
                "available_ingredients": "eggs",
                "steps": None,
            },
            0,
        )

        self.assertEqual(meal.available_ingredients, [])
        self.assertEqual(meal.steps, [])


if __name__ == "__main__":
    unittest.main()
