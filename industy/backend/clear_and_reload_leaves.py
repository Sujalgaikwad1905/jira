"""
Clear old leaves and reload with overlapping dates
"""
import asyncio
import pandas as pd
from datetime import datetime
from db import connect_to_mongo, get_database, close_mongo_connection

async def reload():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("CLEARING AND RELOADING LEAVES")
    print("="*70)
    
    # Delete all old leaves
    result = await db.leaves.delete_many({})
    print(f"\n🗑️ Deleted {result.deleted_count} old leave records")
    
    # Load new ones
    csv_path = "d:/working/industy/uploads/test.csv"
    df = pd.read_csv(csv_path)
    print(f"📂 Loaded CSV: {len(df)} rows")
    
    records = []
    for idx, row in df.iterrows():
        email = str(row["employee_email"]).strip().lower()
        start = pd.to_datetime(row["leave_start"])
        end = pd.to_datetime(row["leave_end"])
        
        record = {
            "employee_email": email,
            "leave_start": start,
            "leave_end": end,
            "file_id": "reload",
            "uploaded_at": datetime.utcnow()
        }
        records.append(record)
        print(f"  {idx+1}. {email}: {start.date()} to {end.date()}")
    
    if records:
        await db.leaves.insert_many(records)
        print(f"\n✅ Inserted {len(records)} new leave records")
    
    print("="*70)
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(reload())
