import unittest

from providers.ai import build_system_prompt, build_user_prompt


class PromptTests(unittest.TestCase):
    def test_system_prompt_uses_english(self):
        prompt = build_system_prompt("en")

        self.assertIn("Always respond in English", prompt)
        self.assertIn('"meals"', prompt)

    def test_system_prompt_uses_indonesian(self):
        prompt = build_system_prompt("id")

        self.assertIn("Always respond in Indonesian", prompt)

    def test_user_prompt_contains_inputs(self):
        prompt = build_user_prompt("eggs", "Quick", 2, 0)

        self.assertIn("eggs", prompt)
        self.assertIn("Quick", prompt)
        self.assertIn("2", prompt)

    def test_retry_prompt_requests_different_ideas(self):
        prompt = build_user_prompt("eggs", "Quick", 2, 1)

        self.assertIn("different ideas", prompt)


if __name__ == "__main__":
    unittest.main()
