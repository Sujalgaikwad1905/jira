"""
Test script to verify the complete JIRA sync process
"""
import asyncio
from datetime import datetime
from db.mongodb import connect_to_mongo, get_database
from services.jira_service import jira_service, JiraTask
from models.jira import JiraCredentialsCreate

async def test_sync_process():
    print("🔍 Testing JIRA sync process...")
    
    # Connect to database
    await connect_to_mongo()
    db = get_database()
    
    # Check initial state
    tasks_collection = db.jira_tasks
    initial_count = await tasks_collection.count_documents({})
    print(f"📊 Initial tasks in database: {initial_count}")
    
    # Test storing sample tasks directly to verify storage works
    print("\n📝 Testing direct task storage...")
    sample_tasks = [
        JiraTask(
            id="",
            user_id="test_user_123",
            jira_id="test_1",
            key="PROJ-1",
            summary="Test task 1",
            status="To Do",
            priority="High",
            assignee="Test User",
            assignee_email="test@example.com",
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            duedate=datetime.utcnow(),
            project_key="PROJ",
            project_name="Test Project",
            issue_type="Task"
        ),
        JiraTask(
            id="",
            user_id="test_user_123",
            jira_id="test_2", 
            key="PROJ-2",
            summary="Test task 2",
            status="In Progress",
            priority="Medium",
            assignee="Test User 2",
            assignee_email="test2@example.com",
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            duedate=datetime.utcnow(),
            project_key="PROJ",
            project_name="Test Project",
            issue_type="Story"
        )
    ]
    
    # Store the tasks using the service method
    store_result = await jira_service.store_jira_tasks("test_user_123", sample_tasks)
    print(f"💾 Storage result: {store_result}")
    
    # Check count after storage
    after_store_count = await tasks_collection.count_documents({})
    print(f"📊 Tasks after storage: {after_store_count}")
    
    # Check tasks for the specific user
    user_task_count = await tasks_collection.count_documents({"user_id": "test_user_123"})
    print(f"📊 Tasks for test_user_123: {user_task_count}")
    
    # Fetch and display sample
    if user_task_count > 0:
        print("\n📋 Sample stored tasks:")
        async for task in tasks_collection.find({"user_id": "test_user_123"}).limit(5):
            print(f"  - {task['key']}: {task['summary']} (Status: {task['status']})")
    
    # Clean up test data
    await tasks_collection.delete_many({"user_id": "test_user_123"})
    final_count = await tasks_collection.count_documents({})
    print(f"🧹 Final task count after cleanup: {final_count}")
    
    print("\n✅ JIRA sync process test completed!")

if __name__ == "__main__":
    asyncio.run(test_sync_process())