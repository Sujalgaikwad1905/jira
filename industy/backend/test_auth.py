"""
Test script to verify authentication is working
"""
import asyncio
from services.auth_service import auth_service
from datetime import timedelta

async def test_auth():
    print("=" * 50)
    print("Testing Authentication Flow")
    print("=" * 50)
    
    # Test 1: Create a token
    print("\n1. Creating test token...")
    test_email = "test@example.com"
    token = auth_service.create_access_token(
        data={"sub": test_email},
        expires_delta=timedelta(minutes=30)
    )
    print(f"✓ Token created: {token[:50]}...")
    
    # Test 2: Verify the token
    print("\n2. Verifying token...")
    token_data = await auth_service.verify_token(token)
    if token_data and token_data.email == test_email:
        print(f"✓ Token verified successfully for: {token_data.email}")
    else:
        print("✗ Token verification failed!")
        return
    
    # Test 3: Check secret key
    print("\n3. Checking configuration...")
    print(f"Secret Key: {auth_service.secret_key[:20]}...")
    print(f"Algorithm: {auth_service.algorithm}")
    print(f"Token Expire: {auth_service.access_token_expire_minutes} minutes")
    
    print("\n" + "=" * 50)
    print("✓ All authentication tests passed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_auth())
