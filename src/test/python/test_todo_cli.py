import os
import pytest
from todo_cli import load_tasks, save_tasks, add_task, delete_task, TASKS_FILE

# --- Setup/Teardown Function ---
def setup_function():
    """Ensures the tasks file is cleaned up before and after each test."""
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def teardown_function():
    """Clean up after test methods."""
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

# --- Test Functions ---

def test_initial_load_returns_empty_list():
    """Test loading an empty list when the file does not exist."""
    tasks = load_tasks()
    assert tasks == []
    assert not os.path.exists(TASKS_FILE)

def test_add_and_save_task():
    """Test adding a task and verifying it's saved and reloaded."""
    tasks = load_tasks() # Should be empty
    add_task(tasks, "Pay bills")
    
    # Check in-memory list
    assert len(tasks) == 1
    assert tasks[0] == "Pay bills"
    
    # Check saved content by reloading
    reloaded_tasks = load_tasks()
    assert reloaded_tasks == ["Pay bills"]

def test_add_multiple_tasks():
    """Test adding multiple tasks maintains order."""
    tasks = load_tasks()
    add_task(tasks, "Task one")
    add_task(tasks, "Task two")
    
    reloaded_tasks = load_tasks()
    assert len(reloaded_tasks) == 2
    assert reloaded_tasks[0] == "Task one"
    assert reloaded_tasks[1] == "Task two"

def test_delete_task_success():
    """Test successful deletion of a task by 1-based index."""
    # Setup: Manually save initial tasks
    initial_tasks = ["A. Read book", "B. Go shopping", "C. Exercise"]
    save_tasks(initial_tasks)
    
    # Load and delete the second task (index '2')
    current_tasks = load_tasks()
    delete_task(current_tasks, "2")
    
    # Check the result
    assert len(current_tasks) == 2
    assert current_tasks == ["A. Read book", "C. Exercise"]
    assert load_tasks() == ["A. Read book", "C. Exercise"] # Verify file update

def test_delete_task_invalid_index_no_change():
    """Test deletion with an index out of bounds maintains state."""
    tasks = ["Only one task"]
    save_tasks(tasks)
    
    current_tasks = load_tasks()
    delete_task(current_tasks, "10") # Invalid index
    
    # The list and file should remain unchanged
    assert current_tasks == ["Only one task"]
    assert load_tasks() == ["Only one task"]

def test_delete_task_invalid_input_type():
    """Test deletion with non-integer input."""
    tasks = ["Test task"]
    save_tasks(tasks)
    
    current_tasks = load_tasks()
    # Assuming delete_task handles non-integer input gracefully (e.g., printing error)
    # The assert here checks that the list state remains unchanged.
    delete_task(current_tasks, "three") 
    
    assert current_tasks == ["Test task"]
