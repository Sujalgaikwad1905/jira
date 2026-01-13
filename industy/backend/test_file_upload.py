"""
Test file upload functionality
"""
import asyncio
import aiohttp
import json

async def test_file_upload():
    url = "http://127.0.0.1:8000/api/files/upload"
    
    # Read the test CSV file
    with open("uploads/test_upload.csv", "rb") as f:
        file_content = f.read()
    
    print("Testing file upload...")
    
    # Create form data manually
    data = aiohttp.FormData()
    data.add_field('file', file_content, filename='test_upload.csv', content_type='text/csv')
    
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(url, data=data)
            print(f"Status: {response.status}")
            
            if response.status == 200:
                result = await response.json()
                print(f"Upload successful: {json.dumps(result, indent=2)}")
            else:
                error_text = await response.text()
                print(f"Upload failed: {response.status} - {error_text}")
                
        except Exception as e:
            print(f"Error during upload: {e}")

if __name__ == "__main__":
    asyncio.run(test_file_upload())