"""
Prepare for fresh demo:
1. Ensure all tasks assigned to sujalgaikwadusa@gmail.com
2. Clear all leaves and risks
3. Ready for fresh file upload
"""
import asyncio
from db import connect_to_mongo, get_database, close_mongo_connection

async def prepare():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("🧹 PREPARING FOR FRESH DEMO")
    print("="*70)
    
    target_email = "sujalgaikwadusa@gmail.com"
    
    # Step 1: Ensure all tasks assigned to demo user
    print("\n[1/3] Assigning all tasks to sujalgaikwadusa@gmail.com...")
    result = await db.jira_tasks.update_many(
        {},
        {"$set": {"assignee_email": target_email, "assignee": "Sujal Gaikwad"}}
    )
    print(f"   ✅ {result.modified_count} tasks updated")
    
    task_count = await db.jira_tasks.count_documents({"assignee_email": target_email})
    print(f"   📋 Total tasks for {target_email}: {task_count}")
    
    # Step 2: Clear all leaves
    print("\n[2/3] Clearing all leave records...")
    result = await db.leaves.delete_many({})
    print(f"   ✅ Deleted {result.deleted_count} leave records")
    
    # Step 3: Clear all risks
    print("\n[3/3] Clearing all risk alerts...")
    result = await db.risk_alerts.delete_many({})
    print(f"   ✅ Deleted {result.deleted_count} risk alerts")
    
    # Verify clean state
    print("\n" + "="*70)
    print("✅ READY FOR FRESH DEMO!")
    print("="*70)
    
    leave_count = await db.leaves.count_documents({})
    risk_count = await db.risk_alerts.count_documents({})
    
    print(f"\n📊 Current State:")
    print(f"   Tasks: {task_count} (all assigned to {target_email})")
    print(f"   Leaves: {leave_count} (cleaned)")
    print(f"   Risks: {risk_count} (cleaned)")
    
    print("\n📋 Tasks waiting for risk detection:")
    async for task in db.jira_tasks.find({"assignee_email": target_email}):
        key = task.get('key')
        due = task.get('duedate')
        summary = task.get('summary', 'N/A')
        print(f"   {key}: {summary} - Due: {due.date() if due else 'N/A'}")
    
    print("\n" + "="*70)
    print("🎬 NEXT STEPS FOR DEMO:")
    print("="*70)
    print("\n1. Upload the file:")
    print("   File: d:\\working\\industy\\uploads\\fresh_demo.csv")
    print("   Contains: sujalgaikwadusa@gmail.com leave from 2025-12-10 to 2026-01-10")
    print("\n2. PowerShell command:")
    print("   $form = @{ file = Get-Item 'd:\\working\\industy\\uploads\\fresh_demo.csv' }")
    print("   Invoke-RestMethod -Uri 'http://localhost:8000/api/files/upload' -Method Post -Form $form")
    print("\n3. Wait 3 seconds, then check risks:")
    print("   Start-Sleep -Seconds 3")
    print("   Invoke-RestMethod -Uri 'http://localhost:8000/api/risks' | ConvertTo-Json")
    print("\n4. Expected result:")
    print("   🚨 8 HIGH priority risk alerts for all tasks!")
    print("="*70 + "\n")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(prepare())
