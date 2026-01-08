import asyncio
from db.mongodb import connect_to_mongo, get_database, close_mongo_connection

async def test_db():
    try:
        print("Connecting to MongoDB...")
        await connect_to_mongo()
        db = get_database()
        print(f"Database connected: {db.name}")
        
        # Test a simple operation
        test_collection = db.test
        await test_collection.insert_one({"test": "connection"})
        print("Database operation successful")
        
        await close_mongo_connection()
        print("Database connection closed")
    except Exception as e:
        print(f"Database test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_db())