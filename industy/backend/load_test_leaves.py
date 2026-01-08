"""
Manually load leaves from test.csv
"""
import asyncio
import pandas as pd
from datetime import datetime
from db import connect_to_mongo, get_database, close_mongo_connection

async def load_leaves():
    await connect_to_mongo()
    db = get_database()
    
    print("\n" + "="*70)
    print("LOADING LEAVES FROM test.csv")
    print("="*70)
    
    # Read the CSV file
    csv_path = "d:/working/industy/uploads/test.csv"
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\n✅ Loaded CSV: {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
        records = []
        for idx, row in df.iterrows():
            email = str(row["employee_email"]).strip().lower()
            start = pd.to_datetime(row["leave_start"])  # Keep as datetime
            end = pd.to_datetime(row["leave_end"])  # Keep as datetime
            
            record = {
                "employee_email": email,
                "leave_start": start,
                "leave_end": end,
                "file_id": "manual_upload",
                "uploaded_at": datetime.utcnow()
            }
            records.append(record)
            print(f"  {idx+1}. {email}: {start.date()} to {end.date()}")
        
        # Insert into database
        if records:
            result = await db.leaves.insert_many(records)
            print(f"\n✅ Inserted {len(records)} leave records")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("="*70)
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(load_leaves())
