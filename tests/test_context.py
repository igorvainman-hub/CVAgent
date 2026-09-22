import unittest

import context


class ContextTests(unittest.TestCase):
    def test_profile_data_is_loaded_into_prompt(self):
        self.assertTrue(context.linkedin.strip())
        self.assertTrue(context.summary.strip())
        self.assertIn(context.summary, context.TWIN_SYSTEM_PROMPT)
        self.assertIn(context.linkedin, context.TWIN_SYSTEM_PROMPT)

    def test_profile_files_are_project_files(self):
        self.assertEqual(context.LINKEDIN_PATH.name, "linkedin.pdf")
        self.assertEqual(context.SUMMARY_PATH.name, "summary.txt")
        self.assertTrue(context.LINKEDIN_PATH.is_file())
        self.assertTrue(context.SUMMARY_PATH.is_file())


if __name__ == "__main__":
    unittest.main()