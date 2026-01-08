"""
Fix the assignee emails in JIRA tasks to match the leave data emails
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database

# Mapping from JIRA display names to correct email addresses
EMAIL_MAPPING = {
    'sairaj.22310237': 'sairaj.22310237@viit.ac.in',
    '20_krishna tolambe': 'krishna.22310498@viit.ac.in',  # Assuming this is the same person with different casing
    'ayush.22311943': 'ayush.22311943@viit.ac.in',
    'krishna.22310498': 'krishna.22310498@viit.ac.in',  # Direct mapping if it exists
    '20_krishna tolambe'.lower(): 'krishna.22310498@viit.ac.in',  # Lowercase version
    'unassigned': '',  # Keep unassigned as empty
}

async def fix_assignee_emails():
    await connect_to_mongo()
    db = get_database()
    
    print("Before fixing emails:")
    
    # Count tasks with and without email
    tasks_without_email = await db.jira_tasks.count_documents({"assignee_email": {"$in": ["", None]}})
    tasks_with_email = await db.jira_tasks.count_documents({"assignee_email": {"$ne": ""}})
    
    print(f"Tasks without email: {tasks_without_email}")
    print(f"Tasks with email: {tasks_with_email}")
    
    # Show tasks that need fixing
    print("\nTasks that need email fixing:")
    async for task in db.jira_tasks.find({"assignee_email": {"$in": ["", None]}, "assignee": {"$ne": "Unassigned"}}).limit(10):
        print(f"  - {task['key']}: Assignee='{task['assignee']}', Email='{task['assignee_email']}'")
    
    # Update tasks based on assignee name
    update_count = 0
    async for task in db.jira_tasks.find():
        assignee_lower = task['assignee'].lower().strip() if task['assignee'] else ''
        
        # Look for email in mapping
        new_email = EMAIL_MAPPING.get(assignee_lower)
        
        if new_email is not None and task['assignee_email'] != new_email:
            # Update the task with the correct email
            await db.jira_tasks.update_one(
                {"_id": task["_id"]},
                {"$set": {"assignee_email": new_email}}
            )
            print(f"  Fixed {task['key']}: {task['assignee']} -> {new_email}")
            update_count += 1
    
    print(f"\nUpdated {update_count} tasks with correct email addresses")
    
    # Show final counts
    tasks_without_email_after = await db.jira_tasks.count_documents({"assignee_email": {"$in": ["", None]}})
    tasks_with_email_after = await db.jira_tasks.count_documents({"assignee_email": {"$ne": ""}})
    
    print(f"After fixing:")
    print(f"Tasks without email: {tasks_without_email_after}")
    print(f"Tasks with email: {tasks_with_email_after}")
    
    print("\nSample of updated tasks:")
    async for task in db.jira_tasks.find({"assignee_email": {"$ne": ""}}).limit(5):
        print(f"  - {task['key']}: {task['assignee']} ({task['assignee_email']})")

if __name__ == "__main__":
    asyncio.run(fix_assignee_emails())