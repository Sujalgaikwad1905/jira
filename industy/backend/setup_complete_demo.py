"""
Complete demo setup:
1. Assign all tasks to sujalgaikwadusa@gmail.com
2. Clear old risks and leaves
3. Load new leave data
4. Trigger risk analysis
5. Show results
"""
import asyncio
import pandas as pd
from datetime import datetime
from db import connect_to_mongo, get_database, close_mongo_connection
from services.risk_service import run_risk_analysis

async def setup_demo():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("🚀 COMPLETE DEMO SETUP")
    print("="*70)
    
    target_email = "sujalgaikwadusa@gmail.com"
    
    # Step 1: Reassign all tasks
    print("\n[1/5] Reassigning all tasks to sujalgaikwadusa@gmail.com...")
    result = await db.jira_tasks.update_many(
        {},
        {"$set": {"assignee_email": target_email, "assignee": "Sujal Gaikwad"}}
    )
    print(f"   ✅ Updated {result.modified_count} tasks")
    
    # Step 2: Clear old risks
    print("\n[2/5] Clearing old risk alerts...")
    result = await db.risk_alerts.delete_many({})
    print(f"   ✅ Deleted {result.deleted_count} old risks")
    
    # Step 3: Clear old leaves
    print("\n[3/5] Clearing old leave records...")
    result = await db.leaves.delete_many({})
    print(f"   ✅ Deleted {result.deleted_count} old leaves")
    
    # Step 4: Load new leave data
    print("\n[4/5] Loading new leave data...")
    csv_path = "d:/working/industy/uploads/demo_sujal.csv"
    df = pd.read_csv(csv_path)
    
    records = []
    for idx, row in df.iterrows():
        email = str(row["employee_email"]).strip().lower()
        start = pd.to_datetime(row["leave_start"])
        end = pd.to_datetime(row["leave_end"])
        
        record = {
            "employee_email": email,
            "leave_start": start,
            "leave_end": end,
            "file_id": "demo_setup",
            "uploaded_at": datetime.utcnow()
        }
        records.append(record)
        print(f"   📅 {email}: {start.date()} to {end.date()}")
    
    if records:
        await db.leaves.insert_many(records)
        print(f"   ✅ Inserted {len(records)} leave records")
    
    # Step 5: Run risk analysis
    print("\n[5/5] Running risk analysis...")
    risks = await run_risk_analysis()
    print(f"   ✅ Created {len(risks)} risk alerts")
    
    # Show summary
    print("\n" + "="*70)
    print("📊 DEMO READY!")
    print("="*70)
    
    # Count tasks
    task_count = await db.jira_tasks.count_documents({"assignee_email": target_email})
    print(f"\n✅ Tasks assigned to {target_email}: {task_count}")
    
    # Show tasks with due dates
    print("\n📋 Tasks:")
    async for task in db.jira_tasks.find({"assignee_email": target_email}):
        key = task.get('key')
        due = task.get('duedate')
        summary = task.get('summary', 'N/A')
        print(f"  {key}: {summary} - Due: {due.date() if due else 'N/A'}")
    
    # Show leave
    print(f"\n🏖️ Leave Period:")
    async for leave in db.leaves.find({"employee_email": target_email}):
        start = leave.get('leave_start')
        end = leave.get('leave_end')
        print(f"  {target_email}")
        print(f"  From: {start.date() if start else 'N/A'}")
        print(f"  To: {end.date() if end else 'N/A'}")
    
    # Show risks
    print(f"\n🚨 Risk Alerts: {len(risks)}")
    for risk in risks:
        print(f"  ⚠️ {risk['task_key']}: Due {risk['due_date']} (on leave)")
    
    print("\n" + "="*70)
    print("✅ DEMO SETUP COMPLETE!")
    print("\nNext steps:")
    print("  1. Run: curl http://localhost:8000/api/risks")
    print("  2. Or: .\\demo_upload.ps1 (to re-upload file)")
    print("="*70 + "\n")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(setup_demo())
