# 🎬 FRESH DEMO - Complete Instructions

## 🎯 What This Demonstrates

You will show the **complete risk detection flow from scratch**:
1. Upload a CSV file with employee leave dates
2. System automatically processes the file
3. Detects tasks due during leave period
4. Creates HIGH priority risk alerts
5. Manager can view all risks via API

---

## 📁 Files Created for Demo

### 1. CSV File to Upload
**File:** `d:\working\industy\uploads\fresh_demo.csv`

**Content:**
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-10,2026-01-10
```

This represents you taking leave from **Dec 10, 2025 to Jan 10, 2026**.

### 2. Demo Scripts
- `prepare_fresh_demo.py` - Prepares database (clears old data)
- `FRESH_DEMO.ps1` - Complete PowerShell demo with colors!

---

## 🚀 How to Run the Demo

### **Option 1: Automatic Demo (Recommended!)**

Just run this one command:

```powershell
cd d:\working\industy\backend
.\FRESH_DEMO.ps1
```

**This will:**
1. ✅ Prepare database (assign tasks, clear old data)
2. ✅ Show the CSV file content
3. ✅ Upload the file via API
4. ✅ Wait for background processing
5. ✅ Show all 8 risk alerts with colors!

**Interactive:** Press any key to move through each step!

---

### **Option 2: Manual Step-by-Step**

#### Step 1: Prepare Database
```powershell
python prepare_fresh_demo.py
```

This will:
- Assign all 8 tasks to sujalgaikwadusa@gmail.com
- Clear old leaves (0 records)
- Clear old risks (0 records)

#### Step 2: Upload File
```powershell
$form = @{ file = Get-Item 'd:\working\industy\uploads\fresh_demo.csv' }
Invoke-RestMethod -Uri 'http://localhost:8000/api/files/upload' -Method Post -Form $form
```

#### Step 3: Wait for Processing
```powershell
Start-Sleep -Seconds 3
```

#### Step 4: Check Risks
```powershell
Invoke-RestMethod -Uri 'http://localhost:8000/api/risks' | ConvertTo-Json
```

---

## 📊 Expected Results

### After Upload:
```json
{
  "id": "...",
  "filename": "fresh_demo.csv",
  "status": "processing"
}
```

### After Risk Check (8 alerts!):
```json
[
  {
    "task_key": "SCRUM-1",
    "assignee": "sujalgaikwadusa@gmail.com",
    "due_date": "2025-12-19",
    "leave_start": "2025-12-10",
    "leave_end": "2026-01-10",
    "risk_level": "HIGH",
    "status": "OPEN"
  },
  ... (7 more tasks)
]
```

**All 8 tasks** have due dates between Dec 10, 2025 and Jan 10, 2026, so **all trigger risk alerts**!

---

## 🎭 Demo Talking Points

### 1. **The Problem**
"Employees take leave, but their tasks are still due. This creates delivery risks that managers don't know about until it's too late."

### 2. **The Solution**
"Our system automatically detects when task due dates overlap with employee leave periods."

### 3. **The Demo**
"Watch what happens when sujalgaikwadusa@gmail.com submits a leave request..."

**[Upload the file]**

### 4. **The Magic**
"The system is now:
- Reading the CSV file
- Checking all 8 Jira tasks assigned to this user
- Comparing due dates with leave dates
- Creating risk alerts automatically"

**[Wait 3 seconds]**

### 5. **The Result**
"Let's check the risk alerts..."

**[Show 8 HIGH priority alerts]**

### 6. **The Impact**
"Now the manager can:
- See all affected tasks at a glance
- Reassign tasks to available team members
- Adjust timelines before deadlines are missed
- Proactively manage delivery risks"

---

## 🔄 Reset for Another Demo

If you want to run the demo again:

```powershell
# Just run the demo script again - it auto-prepares!
.\FRESH_DEMO.ps1
```

Or manually:
```powershell
python prepare_fresh_demo.py
```

---

## 🎯 Key Features Demonstrated

✅ **File Upload** - CSV/Excel support  
✅ **Automatic Processing** - Background task  
✅ **Smart Detection** - Email + date matching  
✅ **Risk Alerts** - HIGH priority notifications  
✅ **Manager Dashboard** - API returns all risks  
✅ **No Manual Intervention** - Fully automated  

---

## 📝 Technical Details

### Tasks in Database:
- **8 tasks** all assigned to sujalgaikwadusa@gmail.com
- Due dates: Dec 16, 17, 19, 24, 25, 31 (2025) and Jan 3 (2026)

### Leave Data:
- Employee: sujalgaikwadusa@gmail.com
- Period: Dec 10, 2025 to Jan 10, 2026

### Risk Detection Logic:
```
For each task:
  IF task.assignee_email == leave.employee_email
  AND leave.start <= task.due_date <= leave.end
  THEN create HIGH priority risk alert
```

### Result:
All 8 tasks fall within the leave period → **8 risk alerts created!**

---

## 🎊 Success Indicators

During the demo, you should see:

1. ✅ File uploaded successfully (200 OK)
2. ✅ Processing status in response
3. ✅ 8 risk alerts returned by API
4. ✅ All alerts show:
   - Correct assignee email
   - Task due dates within leave period
   - HIGH risk level
   - OPEN status

---

## 💡 If Something Goes Wrong

### No risks created?
```powershell
# Manually trigger risk analysis
Invoke-RestMethod -Uri 'http://localhost:8000/api/risks/check'
```

### Want to verify database?
```powershell
python check_data.py
```

### Want to reset everything?
```powershell
python prepare_fresh_demo.py
```

---

## 🚀 You're Ready!

Just run:
```powershell
.\FRESH_DEMO.ps1
```

And watch the magic happen! ✨
