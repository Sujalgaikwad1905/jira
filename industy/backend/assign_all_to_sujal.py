"""
Reassign all tasks to sujalgaikwadusa@gmail.com for demo
"""
import asyncio
from db import connect_to_mongo, get_database, close_mongo_connection

async def reassign():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("REASSIGNING ALL TASKS TO sujalgaikwadusa@gmail.com")
    print("="*70)
    
    target_email = "sujalgaikwadusa@gmail.com"
    
    # Update all tasks
    result = await db.jira_tasks.update_many(
        {},  # All tasks
        {"$set": {"assignee_email": target_email, "assignee": "Sujal Gaikwad"}}
    )
    
    print(f"\n✅ Updated {result.modified_count} tasks")
    print(f"   All tasks now assigned to: {target_email}")
    
    # Show updated tasks
    print("\n📋 Updated Tasks:")
    async for task in db.jira_tasks.find():
        key = task.get('key')
        email = task.get('assignee_email')
        due = task.get('duedate')
        print(f"  {key}: {email} - Due: {due.date() if due else 'N/A'}")
    
    print("\n" + "="*70)
    print("✅ All tasks now assigned to sujalgaikwadusa@gmail.com!")
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(reassign())
