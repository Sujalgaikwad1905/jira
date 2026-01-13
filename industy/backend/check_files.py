"""
Check file upload status
"""
import asyncio
from db.mongodb import connect_to_mongo, get_database

async def check_files():
    await connect_to_mongo()
    db = get_database()
    
    # Check files
    print('Recent files:')
    async for file in db.files.find({}).sort('uploaded_at', -1).limit(10):
        print(f'  - {file["filename"]}: {file["status"]} (Records: {file.get("records", 0)}, Size: {file["size"]})')

if __name__ == "__main__":
    asyncio.run(check_files())