import asyncio
from db import connect_to_mongo, get_database, close_mongo_connection

async def check():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*60)
    print("TASKS FOR sujalgaikwadusa@gmail.com")
    print("="*60)
    
    async for task in db.jira_tasks.find({'assignee_email': 'sujalgaikwadusa@gmail.com'}):
        key = task.get('key')
        due = task.get('duedate')
        summary = task.get('summary')
        print(f"\nTask: {key}")
        print(f"  Summary: {summary}")
        print(f"  Due Date: {due}")
        if due:
            print(f"  Due Date (date): {due.date() if hasattr(due, 'date') else due}")
    
    print("\n" + "="*60)
    print("CURRENT LEAVE for sujalgaikwadusa@gmail.com")
    print("="*60)
    
    async for leave in db.leaves.find({'employee_email': 'sujalgaikwadusa@gmail.com'}):
        start = leave.get('leave_start')
        end = leave.get('leave_end')
        print(f"\nLeave Period:")
        print(f"  Start: {start}")
        print(f"  End: {end}")
        if start and end:
            print(f"  Start (date): {start.date() if hasattr(start, 'date') else start}")
            print(f"  End (date): {end.date() if hasattr(end, 'date') else end}")
    
    print("\n" + "="*60)
    
    await close_mongo_connection()

asyncio.run(check())
