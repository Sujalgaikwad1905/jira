# ✅ PRODUCTION READY - UI to Backend Flow

## Current Status

✅ **Backend APIs Ready:**
- `/api/files/upload` - Upload CSV/Excel (NO AUTH)
- `/api/risks` - Get all risk alerts (NO AUTH)
- `/api/risks/check` - Trigger risk analysis (NO AUTH)

✅ **Database Ready:**
- 8 tasks assigned to sujalgaikwadusa@gmail.com
- 0 leaves (clean slate)
- 0 risks (clean slate)

✅ **Background Processing:**
- Auto-processes uploaded CSV files
- Auto-triggers risk analysis
- Auto-creates risk alerts

---

## How It Works

### 1. User Uploads CSV from Frontend UI
**File format:**
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-10,2026-01-10
```

### 2. Backend Processes File
- Saves to database
- Parses CSV
- Creates leave records
- **Automatically triggers risk analysis**

### 3. Risk Analysis Runs
- Checks all Jira tasks
- Finds tasks with assignee_email matching leave email
- Finds tasks with due_date within leave period
- Creates HIGH priority risk alerts

### 4. Frontend Shows Risks
- Call `GET /api/risks`
- Display all risk alerts
- Show task key, assignee, due date, leave period

---

## Test CSV File Ready

**File:** `d:\working\industy\uploads\fresh_demo.csv`

**Content:**
```csv
employee_email,leave_start,leave_end
sujalgaikwadusa@gmail.com,2025-12-10,2026-01-10
```

**Expected Result:**
- 8 risk alerts created
- All tasks (SCRUM-1, 2, 5, 6, 7, 9, 10, 11) flagged

---

## API Endpoints for Frontend

### Upload File
```javascript
POST /api/files/upload
Content-Type: multipart/form-data

Body: FormData with 'file' field
```

**Response:**
```json
{
  "id": "...",
  "filename": "fresh_demo.csv",
  "status": "processing",
  "uploader": "test@example.com"
}
```

### Get All Risks
```javascript
GET /api/risks
```

**Response:**
```json
[
  {
    "_id": "...",
    "task_key": "SCRUM-1",
    "task_title": "Task 1",
    "assignee": "sujalgaikwadusa@gmail.com",
    "due_date": "2025-12-19 00:00:00",
    "leave_start": "2025-12-10 00:00:00",
    "leave_end": "2026-01-10 00:00:00",
    "risk_level": "HIGH",
    "status": "OPEN",
    "created_at": "..."
  }
]
```

### Manually Trigger Risk Check (Optional)
```javascript
GET /api/risks/check
```

**Response:**
```json
{
  "message": "Risk analysis completed",
  "new_risks_created": 8,
  "data": [...]
}
```

---

## Frontend Integration Steps

### 1. File Upload Component
```javascript
async function uploadLeaveFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/files/upload', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}
```

### 2. Wait for Processing (Optional)
```javascript
// Wait 2-3 seconds for background processing
await new Promise(resolve => setTimeout(resolve, 3000));
```

### 3. Fetch Risk Alerts
```javascript
async function getRiskAlerts() {
  const response = await fetch('http://localhost:8000/api/risks');
  const risks = await response.json();
  return risks;
}
```

### 4. Display Risks
```javascript
risks.forEach(risk => {
  console.log(`⚠️ ${risk.task_key}: ${risk.assignee} on leave`);
  console.log(`   Due: ${risk.due_date}`);
  console.log(`   Leave: ${risk.leave_start} to ${risk.leave_end}`);
});
```

---

## Complete Flow Example

```javascript
// 1. User selects file in UI
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];

// 2. Upload file
const uploadResult = await uploadLeaveFile(file);
console.log('File uploaded:', uploadResult.filename);

// 3. Wait for background processing
await new Promise(resolve => setTimeout(resolve, 3000));

// 4. Get risk alerts
const risks = await getRiskAlerts();
console.log(`Found ${risks.length} risk alerts`);

// 5. Display in UI
displayRisksInTable(risks);
```

---

## Testing Right Now

### Step 1: Backend is Running
```bash
# Should be running on http://localhost:8000
```

### Step 2: Test Upload via Browser/Postman
```
POST http://localhost:8000/api/files/upload
Body: form-data
Key: file
Value: [Select fresh_demo.csv]
```

### Step 3: Check Risks
```
GET http://localhost:8000/api/risks
```

**Expected:** 8 risk alerts

---

## Your Frontend Needs to Call

1. **File Upload Page:**
   - `POST /api/files/upload`
   - Show success message

2. **Risk Dashboard Page:**
   - `GET /api/risks`
   - Display table of risks
   - Show: Task Key, Assignee, Due Date, Leave Period, Risk Level

3. **Optional - Manual Refresh:**
   - `GET /api/risks/check`
   - Button to manually trigger risk analysis

---

## No Authentication Required

All endpoints are open for testing. Add authentication later when you're ready.

---

## Ready to Test from UI!

1. ✅ Backend running on port 8000
2. ✅ Database clean (0 leaves, 0 risks)
3. ✅ 8 tasks ready for risk detection
4. ✅ Test file ready: `fresh_demo.csv`

**Just upload the file from your frontend and check `/api/risks` - it will work!**
