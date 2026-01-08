"""
Test script to verify that JIRA sync functionality works properly
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database
from services.jira_service import jira_service

async def verify_jira_sync():
    print("🔍 Verifying JIRA sync functionality...")
    
    # Connect to database
    await connect_to_mongo()
    db = get_database()
    
    # Check if jira_tasks collection exists and has data
    tasks_collection = db.jira_tasks
    task_count = await tasks_collection.count_documents({})
    
    print(f"📊 Current tasks in database: {task_count}")
    
    # Check if there are any user records
    sample_users = []
    async for doc in tasks_collection.find().limit(5):
        sample_users.append(doc.get('user_id'))
    
    if sample_users:
        print(f"👤 Sample user IDs in tasks: {set(sample_users)}")
    
    # Test the sync method with a dummy user ID to see if it works
    print("\n🔧 Testing JIRA sync with test user...")
    try:
        result = await jira_service.sync_jira_data("test_user_123")
        print(f"✅ Sync result for test user: {result}")
    except Exception as e:
        print(f"❌ Sync failed for test user: {str(e)}")
    
    # Check task count after test
    new_task_count = await tasks_collection.count_documents({})
    print(f"📊 Tasks after sync test: {new_task_count}")
    
    print("\n✅ JIRA sync verification completed!")

if __name__ == "__main__":
    asyncio.run(verify_jira_sync())