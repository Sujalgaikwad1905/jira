import asyncio
from db import connect_to_mongo, get_database, close_mongo_connection

async def check_data():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("CHECKING DATABASE DATA")
    print("="*70)
    
    # Check Jira tasks
    print("\n📋 JIRA TASKS:")
    task_count = await db.jira_tasks.count_documents({})
    print(f"Total tasks: {task_count}")
    
    if task_count > 0:
        print("\nSample tasks:")
        async for task in db.jira_tasks.find().limit(5):
            print(f"  - Key: {task.get('key')}")
            print(f"    Assignee Email: {task.get('assignee_email')}")
            print(f"    Due Date: {task.get('duedate')} (type: {type(task.get('duedate'))})")
            print(f"    Summary: {task.get('summary')}")
            print()
    
    # Check leaves
    print("\n🏖️ LEAVES:")
    leave_count = await db.leaves.count_documents({})
    print(f"Total leaves: {leave_count}")
    
    if leave_count > 0:
        print("\nSample leaves:")
        async for leave in db.leaves.find().limit(10):
            print(f"  - Email: {leave.get('employee_email')}")
            print(f"    Start: {leave.get('leave_start')} (type: {type(leave.get('leave_start'))})")
            print(f"    End: {leave.get('leave_end')}")
            print()
    
    # Check risks
    print("\n⚠️ RISK ALERTS:")
    risk_count = await db.risk_alerts.count_documents({})
    print(f"Total risks: {risk_count}")
    
    if risk_count > 0:
        print("\nExisting risks:")
        async for risk in db.risk_alerts.find().limit(5):
            print(f"  - Task: {risk.get('task_key')}")
            print(f"    Assignee: {risk.get('assignee')}")
            print(f"    Status: {risk.get('status')}")
            print()
    
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(check_data())
