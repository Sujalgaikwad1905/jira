# Quick Testing Guide - Leave Risk Alert System

## Prerequisites
1. Backend server running
2. MongoDB connected
3. User logged in
4. Jira connected and synced (to have tasks with assignee emails)

## Step-by-Step Test

### 1. Install Updated Dependencies
```powershell
cd d:\working\industy\backend
pip install -r requirements.txt
```

This will install:
- pandas (for Excel/CSV processing)
- openpyxl (for Excel file support)

### 2. Start the Backend Server
```powershell
cd d:\working\industy\backend
python start_server.py
```

Server should start on http://localhost:8000

### 3. Start the Frontend (in another terminal)
```powershell
cd d:\working\industy\frontend
npm run dev
```

Frontend should start on http://localhost:5173

### 4. Login and Connect Jira
1. Open browser: http://localhost:5173
2. Login with your credentials
3. Go to Integrations → Connect Jira
4. Enter Jira credentials:
   - Domain: https://your-company.atlassian.net
   - Email: your-jira-email@company.com
   - API Token: your-jira-api-token
5. Click "Sync Data" to fetch tasks

### 5. Upload Leave File
1. Go to Data Management page
2. Use the provided test file: `backend/uploads/test_leaves.csv`
   - Or create your own with format: `employee_email,leave_start,leave_end`
3. Upload the file
4. Watch the status change from "processing" → "processed"

### 6. Check Risk Alerts

**Option A: Via API (using browser or Postman)**
```
GET http://localhost:8000/api/risks
```

**Option B: Check backend logs**
Look for messages like:
```
INFO: Inserted 4 leave records
INFO: Triggering risk analysis after leave processing...
INFO: Created risk alert for task PROJ-123 - assignee john.doe@example.com on leave
INFO: Risk analysis completed: 2 new risks created
```

**Option C: Trigger manual risk check**
```
GET http://localhost:8000/api/risks/check
```

Response:
```json
{
  "message": "Risk analysis completed",
  "new_risks_created": 2,
  "data": [
    {
      "task_key": "PROJ-123",
      "task_title": "Implement Feature X",
      "assignee": "john.doe@example.com",
      "due_date": "2025-12-22",
      "leave_start": "2025-12-20",
      "leave_end": "2025-12-25",
      "risk_level": "HIGH",
      "status": "OPEN",
      "created_at": "2025-12-15T10:30:00Z"
    }
  ]
}
```

## Expected Behavior

### When Risk is Detected
- Task due date: 2025-12-22
- Employee leave: 2025-12-20 to 2025-12-25
- Result: ✅ Risk created (due date falls within leave period)

### When No Risk
- Task due date: 2025-12-10
- Employee leave: 2025-12-20 to 2025-12-25
- Result: ⛔ No risk (due date before leave)

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```powershell
pip install pandas openpyxl
```

### Issue: File status stuck on "processing"
**Check:**
1. Backend logs for errors
2. File format is correct (has required columns)
3. Dates are in valid format (YYYY-MM-DD)

**Solution:**
- Check `backend/uploads/` folder for the file
- Verify file columns: employee_email, leave_start, leave_end
- Re-upload with correct format

### Issue: No risks created even with overlapping dates
**Check:**
1. Tasks have assignee_email field populated
2. Assignee email matches leave record email (case-insensitive)
3. Task has a due date

**Debug:**
```python
# In MongoDB shell or Studio 3T
db.jira_tasks.find({}, {key: 1, assignee_email: 1, duedate: 1})
db.leaves.find({}, {employee_email: 1, leave_start: 1, leave_end: 1})
```

### Issue: Tasks don't have assignee_email
**Solution:**
1. Re-sync Jira data to fetch updated task schema
2. Ensure Jira connection is active
3. Check that Jira API returns assignee.emailAddress field

## Test Data Examples

### Leave File (CSV)
```csv
employee_email,leave_start,leave_end
john.doe@company.com,2025-12-20,2025-12-25
jane.smith@company.com,2026-01-05,2026-01-10
```

### Leave File (Excel)
Same columns, save as .xlsx or .xls

### Creating Test Scenario
1. Find a task in Jira with due date in next 2 weeks
2. Note the assignee's email
3. Create leave record with dates covering the due date
4. Upload → Risk should be created

## Verification Checklist

- [ ] Dependencies installed (pandas, openpyxl)
- [ ] Backend server running without errors
- [ ] Jira connected and synced
- [ ] Leave file uploaded successfully
- [ ] File status shows "processed"
- [ ] Backend logs show risk analysis triggered
- [ ] Risk alerts accessible via API
- [ ] Risks show correct task keys and dates

## API Reference

### Upload File
```
POST /api/files/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Body:
- file: <leave.csv or leave.xlsx>
```

### Get All Risks
```
GET /api/risks
Authorization: Bearer <token>

Response: Array of risk alert objects
```

### Trigger Risk Analysis
```
GET /api/risks/check
Authorization: Bearer <token>

Response: {
  message: string,
  new_risks_created: number,
  data: RiskAlert[]
}
```

### Get Files
```
GET /api/files?page=1&size=50
Authorization: Bearer <token>

Response: {
  files: FileUpload[],
  total: number,
  page: number,
  size: number
}
```
