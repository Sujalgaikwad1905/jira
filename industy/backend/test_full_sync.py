"""
Test script to simulate the full JIRA sync process with a mock response
"""
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime
from db.mongodb import connect_to_mongo, get_database
from services.jira_service import jira_service, JiraCredentialsInDB

async def test_full_sync():
    print("🔍 Testing full JIRA sync process...")
    
    # Connect to database
    await connect_to_mongo()
    db = get_database()
    
    # Check initial state
    tasks_collection = db.jira_tasks
    initial_count = await tasks_collection.count_documents({})
    print(f"📊 Initial tasks in database: {initial_count}")
    
    # Create a mock user ID for testing
    test_user_id = "test_sync_user_123"
    
    # Mock JIRA credentials
    mock_credentials = JiraCredentialsInDB(
        id="mock_id",
        user_id=test_user_id,
        email="test@example.com",
        api_token="encrypted_token",
        domain="https://test.atlassian.net",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Mock JIRA API response
    mock_issues_response = [
        {
            "id": "10001",
            "key": "PROJ-1",
            "fields": {
                "summary": "Test task from JIRA",
                "status": {"name": "To Do"},
                "priority": {"name": "High"},
                "assignee": {
                    "displayName": "Test User",
                    "emailAddress": "test@example.com"
                },
                "project": {
                    "key": "PROJ",
                    "name": "Test Project"
                },
                "issuetype": {"name": "Task"},
                "created": "2025-01-01T10:00:00.000+0000",
                "updated": "2025-01-05T15:30:00.000+0000",
                "duedate": "2025-01-15"  # This should be parsed correctly now
            }
        },
        {
            "id": "10002", 
            "key": "PROJ-2",
            "fields": {
                "summary": "Another test task",
                "status": {"name": "In Progress"},
                "priority": {"name": "Medium"},
                "assignee": {
                    "displayName": "Another User", 
                    "emailAddress": "another@example.com"
                },
                "project": {
                    "key": "PROJ",
                    "name": "Test Project"
                },
                "issuetype": {"name": "Story"},
                "created": "2025-01-02T09:00:00.000+0000",
                "updated": "2025-01-06T14:20:00.000+0000",
                "duedate": "2025-01-20"
            }
        }
    ]
    
    # Mock the JIRA service methods
    with patch.object(jira_service, 'get_jira_credentials', return_value=mock_credentials), \
         patch.object(jira_service, 'validate_jira_connection', return_value=True), \
         patch.object(jira_service, 'fetch_jira_projects', return_value=[]), \
         patch.object(jira_service, 'fetch_jira_tasks', return_value=AsyncMock()) as mock_fetch_tasks:
        
        # Mock the fetch_jira_tasks method to return our test tasks
        from services.jira_service import JiraTask
        mock_tasks = [
            JiraTask(
                id="",
                user_id=test_user_id,
                jira_id="10001",
                key="PROJ-1",
                summary="Test task from JIRA",
                status="To Do",
                priority="High",
                assignee="Test User",
                assignee_email="test@example.com",
                created=datetime(2025, 1, 1, 10, 0, 0),
                updated=datetime(2025, 1, 5, 15, 30, 0),
                duedate=datetime(2025, 1, 15),  # This is now a datetime object
                project_key="PROJ",
                project_name="Test Project",
                issue_type="Task"
            ),
            JiraTask(
                id="",
                user_id=test_user_id,
                jira_id="10002",
                key="PROJ-2",
                summary="Another test task",
                status="In Progress",
                priority="Medium",
                assignee="Another User",
                assignee_email="another@example.com",
                created=datetime(2025, 1, 2, 9, 0, 0),
                updated=datetime(2025, 1, 6, 14, 20, 0),
                duedate=datetime(2025, 1, 20),  # This is now a datetime object
                project_key="PROJ",
                project_name="Test Project",
                issue_type="Story"
            )
        ]
        
        mock_fetch_tasks.return_value = mock_tasks
        
        print(f"\n🔄 Running sync for user: {test_user_id}")
        sync_result = await jira_service.sync_jira_data(test_user_id)
        print(f"✅ Sync result: {sync_result}")
        
        # Check count after sync
        after_sync_count = await tasks_collection.count_documents({})
        print(f"📊 Total tasks after sync: {after_sync_count}")
        
        # Check tasks for the specific user
        user_task_count = await tasks_collection.count_documents({"user_id": test_user_id})
        print(f"📊 Tasks for {test_user_id}: {user_task_count}")
        
        # Fetch and display sample
        if user_task_count > 0:
            print("\n📋 Sample synced tasks:")
            async for task in tasks_collection.find({"user_id": test_user_id}).limit(5):
                print(f"  - {task['key']}: {task['summary']} (Status: {task['status']}, Due: {task.get('duedate')})")
        
        # Clean up test data
        await tasks_collection.delete_many({"user_id": test_user_id})
        final_count = await tasks_collection.count_documents({})
        print(f"🧹 Final task count after cleanup: {final_count}")
    
    print("\n✅ Full JIRA sync test completed!")

if __name__ == "__main__":
    asyncio.run(test_full_sync())