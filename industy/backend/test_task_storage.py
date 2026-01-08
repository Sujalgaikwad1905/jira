"""
Test script to verify that JIRA tasks are properly stored in MongoDB
"""
import asyncio
from datetime import datetime
from db.mongodb import connect_to_mongo, get_database

async def test_task_storage():
    print("Testing JIRA task storage...")
    
    # Connect to database first
    await connect_to_mongo()
    
    # Get database connection
    db = get_database()
    tasks_collection = db.jira_tasks
    
    # Test inserting a sample task
    sample_task = {
        "user_id": "test_user_123",
        "jira_id": "test_jira_123",
        "key": "TEST-123",
        "summary": "Test task for storage verification",
        "status": "To Do",
        "priority": "High",
        "assignee": "Test User",
        "assignee_email": "test@example.com",
        "created": datetime.utcnow(),
        "updated": datetime.utcnow(),
        "duedate": datetime.utcnow(),
        "project_key": "TEST",
        "project_name": "Test Project",
        "issue_type": "Task"
    }
    
    # Insert the test task
    result = await tasks_collection.insert_one(sample_task)
    print(f"✅ Inserted test task with ID: {result.inserted_id}")
    
    # Count tasks for this user
    task_count = await tasks_collection.count_documents({"user_id": "test_user_123"})
    print(f"📊 Total tasks for test user: {task_count}")
    
    # Fetch and display the task
    task = await tasks_collection.find_one({"_id": result.inserted_id})
    print(f"📋 Retrieved task: {task['key']} - {task['summary']}")
    
    # Clean up - remove test task
    await tasks_collection.delete_one({"_id": result.inserted_id})
    print("🧹 Cleaned up test task")
    
    final_count = await tasks_collection.count_documents({"user_id": "test_user_123"})
    print(f"📊 Final task count: {final_count}")
    
    print("✅ Task storage test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_task_storage())