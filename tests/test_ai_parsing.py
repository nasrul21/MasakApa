import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import providers.ai as ai
from errors import AIRequestError, AIResponseError


def fake_client(content: str):
    message = SimpleNamespace(content=content)
    response = SimpleNamespace(choices=[SimpleNamespace(message=message)])
    completions = SimpleNamespace(create=lambda **kwargs: response)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def failing_client(error: Exception):
    def create(**kwargs):
        raise error

    completions = SimpleNamespace(create=create)
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def meal_payload(count: int = 4) -> str:
    meals = [
        {
            "name": f"Meal {index}",
            "duration_minutes": 10,
            "steps": ["Cook"],
        }
        for index in range(count)
    ]
    return json.dumps({"meals": meals})


class AIParsingTests(unittest.TestCase):
    def generate(self, content: str):
        with patch.object(ai, "client", fake_client(content)), patch.object(
            ai,
            "settings",
            SimpleNamespace(ai_model="test-model"),
        ):
            return ai.generate_meal_ideas(
                ingredients="eggs",
                mood="Quick",
                servings=2,
                language="en",
                generation_number=0,
            )

    def test_valid_json_is_converted_to_meals(self):
        meals = self.generate(meal_payload(1))

        self.assertEqual(len(meals), 1)
        self.assertEqual(meals[0].name, "Meal 0")

    def test_markdown_json_is_supported_and_limited_to_three_meals(self):
        meals = self.generate(f"```json\n{meal_payload()}\n```")

        self.assertEqual(len(meals), 3)

    def test_explanatory_text_and_thinking_blocks_are_ignored(self):
        content = (
            "<think>Need to return the recipes.</think>\n"
            "Here is the JSON:\n"
            f"{meal_payload(1)}\n"
            "Hope this helps!"
        )

        meals = self.generate(content)

        self.assertEqual(len(meals), 1)

    def test_invalid_json_raises_response_error(self):
        with self.assertRaises(AIResponseError):
            self.generate("not json")

    def test_missing_meals_raises_response_error(self):
        with self.assertRaises(AIResponseError):
            self.generate("{}")

    def test_missing_seasoning_is_added_to_cooking_steps(self):
        content = json.dumps(
            {
                "meals": [
                    {
                        "name": "Eggs",
                        "missing_ingredients": ["salt"],
                        "steps": ["Cook the eggs"],
                    }
                ]
            }
        )

        meals = self.generate(content)

        self.assertIn("salt", meals[0].steps[-1].lower())

    def test_ollama_connection_failure_becomes_request_error(self):
        with patch.object(
            ai,
            "client",
            failing_client(ConnectionError("Ollama is offline")),
        ), patch.object(
            ai,
            "settings",
            SimpleNamespace(ai_model="test-model"),
        ):
            with self.assertRaises(AIRequestError):
                ai.generate_meal_ideas(
                    ingredients="eggs",
                    mood="Quick",
                    servings=2,
                    language="en",
                    generation_number=0,
                )


if __name__ == "__main__":
    unittest.main()
