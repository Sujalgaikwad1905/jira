"""
Script to check the current state of leaves collection and file processing
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database

async def check_leaves_state():
    print("🔍 Checking current state of leaves collection...")
    
    # Connect to database
    await connect_to_mongo()
    db = get_database()
    
    # Check leaves collection
    leaves_collection = db.leaves
    leaves_count = await leaves_collection.count_documents({})
    print(f"📊 Leaves collection count: {leaves_count}")
    
    if leaves_count > 0:
        print("📋 Sample leave records:")
        async for leave in leaves_collection.find().limit(5):
            print(f"  - Email: {leave['employee_email']}")
            print(f"    Leave Start: {leave['leave_start']}")
            print(f"    Leave End: {leave['leave_end']}")
            print(f"    File ID: {leave.get('file_id', 'N/A')}")
            print(f"    Uploaded At: {leave.get('uploaded_at')}")
            print()
    
    # Check files collection
    files_collection = db.files
    files_count = await files_collection.count_documents({})
    print(f"📁 Files collection count: {files_count}")
    
    if files_count > 0:
        print("📋 Sample file records:")
        async for file in files_collection.find().limit(5):
            print(f"  - Filename: {file['filename']}")
            print(f"    Status: {file['status']}")
            print(f"    Size: {file['size']}")
            print(f"    Content Type: {file['content_type']}")
            print(f"    Uploaded At: {file['uploaded_at']}")
            print(f"    Records: {file.get('records', 'N/A')}")
            print()
    
    # Check if there are any processed files
    processed_files = await files_collection.count_documents({"status": "processed"})
    print(f"✅ Processed files: {processed_files}")
    
    # Check if there are any files with errors
    error_files = await files_collection.count_documents({"status": "error"})
    print(f"❌ Error files: {error_files}")
    
    # Check risk alerts
    risks_collection = db.risk_alerts
    risks_count = await risks_collection.count_documents({})
    print(f"⚠️ Risk alerts: {risks_count}")
    
    print("\n🎯 Summary:")
    print(f"- Leaves: {leaves_count}")
    print(f"- Files: {files_count}")
    print(f"- Processed: {processed_files}")
    print(f"- Errors: {error_files}")
    print(f"- Risks: {risks_count}")

if __name__ == "__main__":
    asyncio.run(check_leaves_state())