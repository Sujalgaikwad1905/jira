"""
Test the complete upload flow
"""
import asyncio
import httpx
import time

async def test_flow():
    base_url = "http://localhost:8000"
    
    print("\n" + "="*70)
    print("🧪 TESTING UPLOAD FLOW")
    print("="*70)
    
    # Test 1: Upload file
    print("\n[1/4] Uploading file...")
    file_path = "d:/working/industy/uploads/fresh_demo.csv"
    
    async with httpx.AsyncClient() as client:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
            response = await client.post(f"{base_url}/api/files/upload", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            print(f"✅ Upload successful!")
            print(f"   File ID: {upload_result.get('id')}")
            print(f"   Filename: {upload_result.get('filename')}")
            print(f"   Status: {upload_result.get('status')}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
            return
    
    # Test 2: Wait for processing
    print("\n[2/4] Waiting for background processing...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    print("✅ Processing should be complete")
    
    # Test 3: Check leaves in database
    print("\n[3/4] Checking database...")
    async with httpx.AsyncClient() as client:
        # Check if we can query (you might need a direct DB check script)
        print("   (DB check would go here)")
    
    # Test 4: Get risks
    print("\n[4/4] Fetching risk alerts...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/api/risks")
        
        if response.status_code == 200:
            risks = response.json()
            print(f"✅ Found {len(risks)} risk alerts")
            
            if len(risks) > 0:
                print("\n📋 Risk Alerts:")
                for idx, risk in enumerate(risks[:5], 1):  # Show first 5
                    print(f"   [{idx}] {risk.get('task_key')}: {risk.get('assignee')}")
                    print(f"       Due: {risk.get('due_date')}")
                    print(f"       Leave: {risk.get('leave_start')} to {risk.get('leave_end')}")
            else:
                print("⚠️ No risks found - checking manually...")
                # Try manual trigger
                response = await client.get(f"{base_url}/api/risks/check")
                result = response.json()
                print(f"   Manual trigger: {result.get('new_risks_created')} risks created")
        else:
            print(f"❌ Failed to get risks: {response.status_code}")
            print(response.text)
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(test_flow())
