"""
Script to manually verify a user's email
"""
import asyncio
import sys
from db import connect_to_mongo, close_mongo_connection, get_database

async def verify_user_by_email(email: str):
    """Manually verify a user's email"""
    try:
        await connect_to_mongo()
        db = get_database()
        users_collection = db.users
        
        # Find user
        user = await users_collection.find_one({"email": email})
        
        if not user:
            print(f"❌ User not found: {email}")
            return False
        
        print(f"\n📧 User: {email}")
        print(f"   Name: {user.get('first_name')} {user.get('last_name')}")
        print(f"   Verified: {user.get('is_verified', False)}")
        print(f"   Role: {user.get('role', 'user')}")
        
        if user.get('is_verified'):
            print("\n✅ User is already verified!")
            return True
        
        # Update user to verified
        result = await users_collection.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
        
        if result.modified_count > 0:
            print(f"\n✅ Successfully verified user: {email}")
            return True
        else:
            print(f"\n❌ Failed to verify user: {email}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    finally:
        await close_mongo_connection()

async def list_all_users():
    """List all users in the database"""
    try:
        await connect_to_mongo()
        db = get_database()
        users_collection = db.users
        
        print("\n" + "=" * 70)
        print("ALL USERS IN DATABASE")
        print("=" * 70)
        
        users = []
        async for user in users_collection.find():
            users.append(user)
        
        if not users:
            print("\n❌ No users found in database")
            return
        
        for idx, user in enumerate(users, 1):
            status = "✅" if user.get('is_verified') else "❌"
            print(f"\n{idx}. {status} {user.get('email')}")
            print(f"   Name: {user.get('first_name')} {user.get('last_name')}")
            print(f"   Verified: {user.get('is_verified', False)}")
            print(f"   Role: {user.get('role', 'user')}")
        
        print("\n" + "=" * 70)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await close_mongo_connection()

async def main():
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python verify_user.py list                    # List all users")
        print("  python verify_user.py <email>                 # Verify specific user")
        print("\nExample:")
        print("  python verify_user.py user@example.com")
        return
    
    command = sys.argv[1]
    
    if command.lower() == "list":
        await list_all_users()
    else:
        await verify_user_by_email(command)

if __name__ == "__main__":
    asyncio.run(main())
