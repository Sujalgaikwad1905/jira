# 🎯 PowerShell Demo Commands

## Option 1: Use the Demo Script (Easiest!)

```powershell
cd d:\working\industy\backend
.\demo_upload.ps1
```

This will:
1. Upload `demo_sujal.csv`
2. Wait 3 seconds
3. Show the risk alert with nice colors!

---

## Option 2: Manual PowerShell Commands

### Upload File
```powershell
$filePath = "d:\working\industy\uploads\demo_sujal.csv"
$url = "http://localhost:8000/api/files/upload"

$form = @{
    file = Get-Item -Path $filePath
}

$response = Invoke-RestMethod -Uri $url -Method Post -Form $form
$response | ConvertTo-Json
```

### Wait for Processing
```powershell
Start-Sleep -Seconds 3
```

### Check Risks
```powershell
$risks = Invoke-RestMethod -Uri "http://localhost:8000/api/risks" -Method Get
$risks | ConvertTo-Json -Depth 5
```

### Filter for Demo User Only
```powershell
$risks | Where-Object { $_.assignee -eq "sujalgaikwadusa@gmail.com" } | ConvertTo-Json -Depth 5
```

---

## Option 3: Quick One-Liners

### Just Check Existing Risks
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/risks" | ConvertTo-Json
```

### Trigger Risk Analysis Manually
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/risks/check" | ConvertTo-Json
```

### Upload and Check in One Command
```powershell
$form = @{ file = Get-Item "d:\working\industy\uploads\demo_sujal.csv" }; Invoke-RestMethod -Uri "http://localhost:8000/api/files/upload" -Method Post -Form $form; Start-Sleep 3; Invoke-RestMethod -Uri "http://localhost:8000/api/risks" | ConvertTo-Json
```

---

## 🎬 Recommended Demo Flow

### Step 1: Clear old risks (optional - for fresh demo)
```powershell
python -c "import asyncio; from db import connect_to_mongo, get_database, close_mongo_connection; async def clear(): await connect_to_mongo(); db = get_database(); result = await db.risk_alerts.delete_many({}); print(f'Cleared {result.deleted_count} risks'); await close_mongo_connection(); asyncio.run(clear())"
```

### Step 2: Run the demo script
```powershell
.\demo_upload.ps1
```

### Step 3: Show the results!
The script will display:
```
🚨 RISK DETECTED FOR DEMO USER!
  Task: SCRUM-5
  Title: test_epic1
  Assignee: sujalgaikwadusa@gmail.com
  Due Date: 2026-01-03
  Leave: 2025-12-25 to 2026-01-10
  Risk Level: HIGH
  Status: OPEN
```

---

## 📊 What This Proves

✅ **File uploaded** → System received leave data
✅ **Background processing** → Automatically processed CSV
✅ **Risk analysis triggered** → Checked all tasks
✅ **Overlap detected** → Task due (Jan 3) falls within leave (Dec 25 - Jan 10)
✅ **Alert created** → HIGH priority risk for manager
✅ **API returns data** → Frontend can display this

---

## 🎯 Demo Talking Points

1. **"Employee requests leave for holidays"** 
   → Upload CSV file

2. **"System automatically processes the request"** 
   → Background task runs

3. **"Checks all assigned Jira tasks"** 
   → Risk analysis engine

4. **"Finds task due during leave period"** 
   → Date overlap detection

5. **"Creates HIGH priority alert"** 
   → Risk notification

6. **"Manager can now take action"** 
   → Reassign, reschedule, or plan backup

---

## ✅ Ready to Go!

Just run:
```powershell
.\demo_upload.ps1
```

And you'll see the risk detection in action! 🚀
