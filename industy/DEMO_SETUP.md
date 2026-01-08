# 🎯 DEMO SETUP FOR sujalgaikwadusa@gmail.com

## Current Situation

**Your Task:**
- **SCRUM-5** assigned to sujalgaikwadusa@gmail.com
- **Due Date:** January 3, 2026 (2026-01-03)

**Current Leave:**
- **From:** December 15, 2025
- **To:** January 5, 2026
- **Status:** ✅ ALREADY OVERLAPS! (Jan 3 is within Dec 15 - Jan 5)

---

## 🎬 Demo Option 1: Show Existing Risk (Easiest!)

The risk already exists! Just show:

```bash
# Get all risks
curl http://localhost:8000/api/risks
```

Look for:
```json
{
  "task_key": "SCRUM-5",
  "assignee": "sujalgaikwadusa@gmail.com",
  "due_date": "2026-01-03",
  "leave_start": "2025-12-15",
  "leave_end": "2026-01-05",
  "risk_level": "HIGH",
  "status": "OPEN"
}
```

✅ **This proves the system works!**

---

## 🎬 Demo Option 2: Upload Fresh Data (More Impressive!)

### Step 1: Clear existing risks
```bash
cd d:\working\industy\backend
python -c "import asyncio; from db import connect_to_mongo, get_database, close_mongo_connection; async def clear(): await connect_to_mongo(); db = get_database(); result = await db.risk_alerts.delete_many({}); print(f'Deleted {result.deleted_count} risks'); await close_mongo_connection(); asyncio.run(clear())"
```

### Step 2: Create demo CSV

**Create file:** `d:\working\industy\uploads\demo_sujal.csv`

```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-25,2026-01-10
```

**Why this works:**
- Task SCRUM-5 is due: **Jan 3, 2026**
- Leave period: **Dec 25, 2025 to Jan 10, 2026**
- **Jan 3 falls within this period** → RISK!

### Step 3: Upload the file
```bash
curl -X POST http://localhost:8000/api/files/upload \
  -F "file=@d:/working/industy/uploads/demo_sujal.csv"
```

### Step 4: Check risks (should auto-create!)
```bash
curl http://localhost:8000/api/risks
```

### Step 5: Or manually trigger
```bash
curl http://localhost:8000/api/risks/check
```

---

## 🎬 Demo Option 3: Different Dates for Variety

### Scenario A: Holiday Break
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-20,2026-01-05
```
- **Story:** "Going home for holidays"
- Task due Jan 3 → Overlaps!

### Scenario B: Medical Leave
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2026-01-01,2026-01-07
```
- **Story:** "Scheduled medical procedure"
- Task due Jan 3 → Overlaps!

### Scenario C: Vacation
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-28,2026-01-06
```
- **Story:** "New Year vacation"
- Task due Jan 3 → Overlaps!

---

## 📊 What to Show in Demo

### 1. Before Upload
```bash
curl http://localhost:8000/api/risks
# Shows: [] or existing risks
```

### 2. Upload Leave File
```bash
curl -X POST http://localhost:8000/api/files/upload \
  -F "file=@uploads/demo_sujal.csv"
```

**Response:**
```json
{
  "id": "...",
  "filename": "demo_sujal.csv",
  "status": "processing",
  "uploader": "test@example.com"
}
```

### 3. After Upload (Auto Risk Detection!)
```bash
curl http://localhost:8000/api/risks
```

**Response:**
```json
[
  {
    "task_key": "SCRUM-5",
    "task_title": "test_epic1",
    "assignee": "sujalgaikwadusa@gmail.com",
    "due_date": "2026-01-03 00:00:00",
    "leave_start": "2025-12-25 00:00:00",
    "leave_end": "2026-01-10 00:00:00",
    "risk_level": "HIGH",
    "status": "OPEN",
    "created_at": "..."
  }
]
```

### 4. Show the Logic
**Point out:**
- ✅ Task assigned to: sujalgaikwadusa@gmail.com
- ✅ Task due: Jan 3, 2026
- ✅ Employee on leave: Dec 25, 2025 - Jan 10, 2026
- ✅ Jan 3 is within leave period
- ✅ System automatically detected risk!
- ✅ Manager can now reassign or adjust timeline

---

## 🎯 Quick Demo Script

### I'll create the demo CSV for you:

**File: `uploads/demo_sujal.csv`**
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-25,2026-01-10
```

### Demo Commands:
```bash
# 1. Show current task
echo "Task SCRUM-5 assigned to sujalgaikwadusa@gmail.com is due Jan 3, 2026"

# 2. Upload leave file
curl -X POST http://localhost:8000/api/files/upload \
  -F "file=@uploads/demo_sujal.csv"

# 3. Check risks (wait 2-3 seconds for background processing)
sleep 3
curl http://localhost:8000/api/risks

# 4. Point out the risk
echo "Risk detected! Task due while employee on leave!"
```

---

## 💡 Key Talking Points for Demo

1. **"Employee submits leave request"** → Upload CSV
2. **"System automatically checks all tasks"** → Background processing
3. **"Finds task due during leave period"** → Risk detection
4. **"Creates HIGH priority alert"** → Risk alert
5. **"Manager can take action"** → Reassign, reschedule, or plan coverage

---

## ✅ Ready to Demo!

Your current setup **already works**! The task and leave overlap.

**Want me to:**
1. Create a fresh demo CSV with clear dates?
2. Clear existing risks so you can show it from scratch?
3. Both?

Just say the word! 🚀
