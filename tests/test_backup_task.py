import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from resource import BaseTask, Database, Oss
from resource.task.backup_task import BackupTaskProcess

@pytest.mark.asyncio
async def test_backup_task_process():
    # Setup mocks
    mock_db = MagicMock(spec=Database)
    mock_oss = MagicMock(spec=Oss)
    mock_task = BaseTask(task_id=1, task_name="TestTask", database_name="db", task_type="backup_task")

    # Mock database method and oss method
    mock_db_method = MagicMock()
    # get_dump_stream returns (process, stream, stderr)
    mock_process = AsyncMock()
    mock_process.wait.return_value = None
    mock_process.returncode = 0

    mock_stream = AsyncMock()
    mock_stderr = AsyncMock()

    mock_db_method.get_dump_stream = AsyncMock(return_value=(mock_process, mock_stream, mock_stderr))

    mock_oss_method = MagicMock()
    mock_oss_method.upload_stream = AsyncMock(return_value=None)

    # Patch GetObjectMethod
    with patch("resource.task.backup_task.GetObjectMethod") as mock_get_obj:
        mock_get_obj.get_database_type.return_value = mock_db_method
        mock_get_obj.get_oss_type.return_value = mock_oss_method

        # Initialize process
        process = BackupTaskProcess(mock_task, mock_db, mock_oss)

        # Run process
        await process.run()

        # Assertions
        assert mock_task.task_status == "FINISHED"
        mock_db_method.get_dump_stream.assert_called_once()
        mock_oss_method.upload_stream.assert_called_once()

@pytest.mark.asyncio
async def test_backup_task_failure():
    # Setup mocks for failure
    mock_db = MagicMock(spec=Database)
    mock_oss = MagicMock(spec=Oss)
    mock_task = BaseTask(task_id=2, task_name="TestTaskFail", database_name="db", task_type="backup_task")

    mock_db_method = MagicMock()
    mock_process = AsyncMock()
    mock_process.wait.return_value = None
    mock_process.returncode = 1 # Failure
    mock_process.terminate = MagicMock()

    mock_stream = AsyncMock()
    mock_stderr = AsyncMock()
    mock_stderr.read = AsyncMock(return_value=b"Error dump")

    mock_db_method.get_dump_stream = AsyncMock(return_value=(mock_process, mock_stream, mock_stderr))

    mock_oss_method = MagicMock()
    mock_oss_method.upload_stream = AsyncMock(return_value=None)

    with patch("resource.task.backup_task.GetObjectMethod") as mock_get_obj:
        mock_get_obj.get_database_type.return_value = mock_db_method
        mock_get_obj.get_oss_type.return_value = mock_oss_method

        process = BackupTaskProcess(mock_task, mock_db, mock_oss)

        # Run process
        await process.run()

        # Assertions
        assert mock_task.task_status == "ERROR"
        mock_process.terminate.assert_called()
