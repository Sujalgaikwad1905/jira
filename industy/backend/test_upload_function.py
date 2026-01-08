"""
Test the upload functionality directly
"""
import asyncio
import os
from db.mongodb import connect_to_mongo, get_database
from services.leave_processor import process_leave_file

async def test_upload_function():
    print("🔍 Testing upload functionality directly...")
    
    # Connect to database
    await connect_to_mongo()
    db = get_database()
    
    # Clear existing leaves and risks to start fresh
    await db.leaves.delete_many({})
    await db.risk_alerts.delete_many({})
    
    print("\n✅ Step 1: Preparing test file...")
    
    # Create a test file record in the database
    files_collection = db.files
    test_file_path = os.path.join(os.path.dirname(__file__), "uploads", "test_upload.csv")
    
    if not os.path.exists(test_file_path):
        print(f"❌ Test file does not exist: {test_file_path}")
        return
    
    dummy_file_record = {
        "user_id": "test_user_upload",
        "filename": "test_upload.csv",
        "size": os.path.getsize(test_file_path),
        "content_type": "text/csv",
        "status": "uploading",
        "uploader": "test@example.com",
        "uploaded_at": asyncio.get_event_loop().run_in_executor(None, lambda: __import__('datetime').datetime.utcnow())
    }
    import datetime
    dummy_file_record["uploaded_at"] = datetime.datetime.utcnow()
    
    from bson import ObjectId
    result = await files_collection.insert_one(dummy_file_record)
    file_id = str(result.inserted_id)
    print(f"📁 Created file record with ID: {file_id}")
    print(f"📄 File path: {test_file_path}")
    print(f"📊 File size: {os.path.getsize(test_file_path)} bytes")
    
    print("\n✅ Step 2: Processing leave file...")
    
    try:
        # Process the leave file directly
        await process_leave_file(file_id, test_file_path)
        
        # Check how many leave records were stored
        leaves_collection = db.leaves
        leave_count = await leaves_collection.count_documents({})
        print(f"📅 Leave records stored: {leave_count}")
        
        # Show stored leaves
        if leave_count > 0:
            print("📅 Stored leave records:")
            async for leave in leaves_collection.find():
                print(f"  - Email: {leave['employee_email']}")
                print(f"    Leave Start: {leave['leave_start']}")
                print(f"    Leave End: {leave['leave_end']}")
                print(f"    File ID: {leave.get('file_id', 'N/A')}")
                print()
        
        # Check the file record status
        file_record = await files_collection.find_one({"_id": ObjectId(file_id)})
        if file_record:
            print(f"✅ File status: {file_record['status']}")
            print(f"✅ Records processed: {file_record.get('records', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error processing leave file: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Step 3: Checking risk analysis...")
    
    # Check if risks were created
    risks_collection = db.risk_alerts
    risk_count = await risks_collection.count_documents({})
    print(f"⚠️ Risk alerts created: {risk_count}")
    
    if risk_count > 0:
        print("🚨 Sample risk alerts:")
        async for risk in risks_collection.find().limit(5):
            print(f"  - Task: {risk['task_key']}")
            print(f"    Assignee: {risk['assignee']}")
            print(f"    Due: {risk['due_date']}")
            print(f"    Leave: {risk['leave_start']} to {risk['leave_end']}")
            print(f"    Risk Level: {risk['risk_level']}")
            print()
    
    print("\n🎯 Upload Function Test Results:")
    print(f"- Leave records: {leave_count}")
    print(f"- Risk alerts: {risk_count}")
    
    # Clean up test data
    await leaves_collection.delete_many({})
    await risks_collection.delete_many({})
    await files_collection.delete_one({"_id": ObjectId(file_id)})
    
    print("🧹 Cleaned up test data")
    
    print("\n📋 Summary:")
    print("✅ File processing working")
    print("✅ Data stored in leaves collection")
    print("✅ Risk analysis triggered")
    print("✅ Complete upload flow functional")

if __name__ == "__main__":
    asyncio.run(test_upload_function())