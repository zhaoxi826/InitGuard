import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_api_flow(client: AsyncClient):
    # 1. Login as admin
    response = await client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. List tasks (should be empty initially)
    response = await client.get("/api/task/list", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 0

    # 3. Create a resource (Database)
    # We need to create a resource first to use its ID in task creation,
    # but the task API might not validate resource existence if we just pass IDs?
    # Actually, let's look at task_api:
    # It calls postgres.add_task.
    # postgres_api.add_task creates BaseTask.
    # It does NOT check if database_id exists in DB (unless foreign key constraint).
    # SQLModel by default doesn't enforce foreign keys in SQLite unless enabled.
    # But let's try to be proper.

    # Create Database Resource
    db_resource = {
        "resource_name": "TestDB",
        "resource_value": {
            "type": "database",
            "database_type": "postgres",
            "host": "localhost",
            "port": 5432,
            "username": "user",
            "password": "password"
        }
    }
    response = await client.post("/api/resource/create", json=db_resource, headers=headers)
    assert response.status_code == 200

    # 4. Create a Task
    task_data = {
        "task_name": "BackupTask1",
        "database_id": 1,
        "oss_id": 1, # Dummy ID
        "database_name": "target_db",
        "task_type": "backup_task"
    }
    response = await client.post("/api/task/create", json=task_data, headers=headers)
    assert response.status_code == 200

    # 5. List tasks again
    response = await client.get("/api/task/list", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["task_name"] == "BackupTask1"

    # 6. Filter tasks
    response = await client.get("/api/task/list?task_type=backup_task", headers=headers)
    assert len(response.json()) == 1

    response = await client.get("/api/task/list?task_type=other_task", headers=headers)
    assert len(response.json()) == 0
