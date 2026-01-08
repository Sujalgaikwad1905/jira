"""
Debug why risks aren't matching
"""
import asyncio
from datetime import datetime
from db import connect_to_mongo, get_database, close_mongo_connection

async def debug():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("DEBUGGING TASK/LEAVE MATCHING")
    print("="*70)
    
    # Get all tasks with emails
    print("\n📋 TASKS:")
    async for task in db.jira_tasks.find():
        email = task.get('assignee_email')
        due = task.get('duedate')
        if email and due:
            due_date = due.date() if isinstance(due, datetime) else due
            print(f"  {task.get('key')}: {email} - Due: {due_date}")
    
    print("\n🏖️ LEAVES:")
    async for leave in db.leaves.find():
        email = leave.get('employee_email')
        start = leave.get('leave_start')
        end = leave.get('leave_end')
        start_date = start.date() if isinstance(start, datetime) else start
        end_date = end.date() if isinstance(end, datetime) else end
        print(f"  {email}: {start_date} to {end_date}")
    
    print("\n🔍 CHECKING OVERLAPS:")
    async for task in db.jira_tasks.find():
        task_email = task.get('assignee_email')
        task_due = task.get('duedate')
        task_key = task.get('key')
        
        if not task_email or not task_due:
            continue
        
        task_email_lower = task_email.lower().strip()
        due_date = task_due.date() if isinstance(task_due, datetime) else task_due
        
        # Find matching leaves
        async for leave in db.leaves.find({"employee_email": task_email_lower}):
            leave_start = leave.get('leave_start')
            leave_end = leave.get('leave_end')
            start_date = leave_start.date() if isinstance(leave_start, datetime) else leave_start
            end_date = leave_end.date() if isinstance(leave_end, datetime) else leave_end
            
            # Check if due date is within leave period
            if start_date <= due_date <= end_date:
                print(f"  ⚠️ OVERLAP: {task_key} ({task_email_lower}) due {due_date} overlaps leave {start_date} to {end_date}")
            else:
                print(f"  ❌ NO OVERLAP: {task_key} ({task_email_lower}) due {due_date} vs leave {start_date} to {end_date}")
    
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(debug())
