"""
Quick script to add assignee_email to existing Jira tasks for testing
"""
import asyncio
from db import connect_to_mongo, get_database, close_mongo_connection

async def add_assignee_emails():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("ADDING ASSIGNEE EMAILS TO JIRA TASKS")
    print("="*70)
    
    # Update all tasks without assignee_email
    tasks = db.jira_tasks
    
    # Get all tasks
    all_tasks = []
    async for task in tasks.find():
        all_tasks.append(task)
    
    print(f"\nFound {len(all_tasks)} tasks")
    
    # Add assignee_email to each task
    updated = 0
    for idx, task in enumerate(all_tasks, 1):
        task_key = task.get('key')
        current_email = task.get('assignee_email')
        
        if current_email:
            print(f"{idx}. {task_key} - Already has email: {current_email}")
            continue
        
        # Assign email based on task number (round-robin through test users)
        test_emails = [
            "sujalgaikwadusa@gmail.com",
            "rahul@gmail.com",
            "priya@gmail.com",
            "aman@gmail.com",
            "sneha@gmail.com",
            "rohit@gmail.com"
        ]
        
        # Pick email based on index
        assigned_email = test_emails[idx % len(test_emails)]
        
        # Update task
        result = await tasks.update_one(
            {"_id": task["_id"]},
            {"$set": {"assignee_email": assigned_email}}
        )
        
        if result.modified_count > 0:
            print(f"{idx}. ✅ {task_key} - Added email: {assigned_email}")
            updated += 1
        else:
            print(f"{idx}. ❌ {task_key} - Failed to update")
    
    print(f"\n✅ Updated {updated} tasks with assignee emails")
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(add_assignee_emails())
