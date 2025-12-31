import pytest
from phase1.service import TodoService, TaskNotFoundError

@pytest.fixture
def service():
    return TodoService()

def test_add_task(service):
    task = service.add("Test Task", "Test Description")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False

def test_list_tasks(service):
    service.add("Task 1")
    service.add("Task 2")
    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2

def test_set_status(service):
    service.add("Task")
    service.set_status(1, True)
    assert service.get_task(1).completed is True
    service.set_status(1, False)
    assert service.get_task(1).completed is False

def test_update_task(service):
    service.add("Old Title", "Old Desc")
    service.update(1, title="New Title")
    task = service.get_task(1)
    assert task.title == "New Title"
    assert task.description == "Old Desc"

def test_delete_task(service):
    service.add("To Delete")
    service.delete(1)
    assert len(service.list_tasks()) == 0
    with pytest.raises(TaskNotFoundError):
        service.get_task(1)
