"""
Check the current state of the system
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database

async def check_state():
    await connect_to_mongo()
    db = get_database()
    
    # Check collections
    collections = await db.list_collection_names()
    print('Collections:', collections)
    
    # Check jira_tasks
    jira_tasks = await db.jira_tasks.count_documents({})
    print(f'JIRA tasks: {jira_tasks}')
    
    # Check leaves
    leaves = await db.leaves.count_documents({})
    print(f'Leaves: {leaves}')
    
    # Check risks
    risks = await db.risk_alerts.count_documents({})
    print(f'Risks: {risks}')
    
    # Check files
    files = await db.files.count_documents({})
    print(f'Files: {files}')
    
    # Show sample tasks if any
    if jira_tasks > 0:
        print('\nSample JIRA tasks:')
        async for task in db.jira_tasks.find().limit(5):
            print(f'  - {task["key"]}: {task["summary"][:50]}... (Assignee: {task.get("assignee_email", "N/A")})')
    
    # Show sample leaves if any
    if leaves > 0:
        print('\nSample leaves:')
        async for leave in db.leaves.find().limit(5):
            print(f'  - {leave["employee_email"]}: {leave["leave_start"]} to {leave["leave_end"]}')
    
    # Show sample risks if any
    if risks > 0:
        print('\nSample risks:')
        async for risk in db.risk_alerts.find().limit(5):
            print(f'  - Task: {risk["task_key"]} (Assignee: {risk["assignee"]}) - Risk: {risk["risk_level"]}')

if __name__ == "__main__":
    asyncio.run(check_state())