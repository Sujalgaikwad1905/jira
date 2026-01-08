"""
Check JIRA credentials and task distribution
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database

async def check_credentials():
    await connect_to_mongo()
    db = get_database()
    
    # Check if there are any JIRA credentials stored
    credentials = await db.jira_credentials.find_one()
    if credentials:
        print('JIRA Credentials found:')
        print(f'  - Domain: {credentials["domain"]}')
        print(f'  - Email: {credentials["email"]}')
        print(f'  - User ID: {credentials["user_id"]}')
        
        # Check if this user has tasks
        user_tasks = await db.jira_tasks.count_documents({'user_id': credentials['user_id']})
        print(f'  - Tasks for this user: {user_tasks}')
    else:
        print('No JIRA credentials found')
        
    # Count tasks by user
    pipeline = [
        {'$group': {'_id': '$user_id', 'count': {'$sum': 1}}}
    ]
    result = []
    async for item in db.jira_tasks.aggregate(pipeline):
        result.append(item)
    print(f'Task distribution by user: {result}')
    
    # Check sample tasks to see assignee data
    print('\nSample tasks with assignee data:')
    async for task in db.jira_tasks.find().limit(10):
        print(f'  - {task["key"]}: Assignee="{task.get("assignee", "N/A")}", Email="{task.get("assignee_email", "N/A")}", DueDate="{task.get("duedate", "N/A")}"')

if __name__ == "__main__":
    asyncio.run(check_credentials())