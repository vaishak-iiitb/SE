import unittest
import os
# Assuming todo_cli.py is imported correctly based on the directory structure
from todo_cli import load_tasks, save_tasks, add_task, delete_task, TASKS_FILE

# ... (The rest of the test_todo_cli.py content is unchanged)
class TestTodoCLI(unittest.TestCase):
    """Tests for the todo_cli.py application functions."""

    def setUp(self):
        """Set up for test methods. Ensures the tasks file is clean."""
        # Remove the file if it exists before each test
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

    def tearDown(self):
        """Clean up after test methods. Removes the tasks file."""
        if os.path.exists(TASKS_FILE):
            os.remove(TASKS_FILE)

    def test_initial_load(self):
        """Test loading an empty list when the file does not exist."""
        tasks = load_tasks()
        self.assertEqual(tasks, [], "Should return an empty list initially.")
    # ... (include all other test_ methods here)
