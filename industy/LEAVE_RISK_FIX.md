# Leave Upload & Risk Alert Fix Summary

## Issues Fixed

### 1. **Missing Assignee Email Field**
**Problem:** Jira tasks were storing only the assignee's display name, not their email. The risk service needs the email to match with leave records.

**Solution:** 
- Added `assignee_email` field to `JiraTask` model
- Modified Jira service to extract and store `emailAddress` from assignee object
- Updated all JiraTask construction sites to include `assignee_email`

**Files Modified:**
- `backend/models/jira.py` - Added `assignee_email` field to JiraTask model
- `backend/services/jira_service.py` - Extract assignee email from Jira API response
- `backend/services/dashboard_service.py` - Include assignee_email when constructing JiraTask
- `backend/services/tasks_service.py` - Include assignee_email when constructing JiraTask

### 2. **Incorrect Field Names in Risk Service**
**Problem:** Risk service was looking for:
- `assignee_email` ✅ (correct)
- `due_date` ❌ (should be `duedate`)
- `task_id` ❌ (should be `key`)

**Solution:** 
- Changed field references to match actual database schema
- Updated risk alert model to use `task_key` instead of `task_id`

**Files Modified:**
- `backend/services/risk_service.py` - Fixed field name references
- `backend/models/risk_alert.py` - Changed `task_id` to `task_key`

### 3. **Date Type Mismatch**
**Problem:** MongoDB date comparison failing due to type mismatch:
- Leave dates stored as Python `date` objects
- Task due dates stored as `datetime` objects
- MongoDB comparison wasn't working properly

**Solution:**
- Added date type conversion in risk service
- Properly convert datetime to date for comparison
- Handle both date and datetime types gracefully

**Files Modified:**
- `backend/services/risk_service.py` - Added date conversion logic

### 4. **Risk Analysis Not Triggered**
**Problem:** Leave file upload wasn't triggering risk analysis automatically.

**Solution:**
- Added automatic risk analysis trigger after leave file processing
- Added proper logging for tracking risk creation

**Files Modified:**
- `backend/services/leave_processor.py` - Added risk analysis trigger

### 5. **CSV File Support Missing**
**Problem:** System only processed .xlsx and .xls files, not CSV files.

**Solution:**
- Added CSV file detection and processing in leave_processor
- Updated file upload endpoint to handle CSV files

**Files Modified:**
- `backend/services/leave_processor.py` - Added CSV support with pandas.read_csv()
- `backend/routers/files.py` - Added .csv to accepted file extensions

### 6. **Missing Dependencies**
**Problem:** pandas and openpyxl were used but not in requirements.txt

**Solution:**
- Added pandas==2.1.4 and openpyxl==3.1.2 to requirements

**Files Modified:**
- `backend/requirements.txt`

## How It Works Now

1. **User uploads leave Excel/CSV file** via Data Management page
   - File format: `employee_email`, `leave_start`, `leave_end`
   - Example: `john.doe@company.com, 2025-12-20, 2025-12-25`

2. **Leave Processor**:
   - Reads the file (Excel or CSV)
   - Validates required columns
   - Converts dates to proper date objects
   - Stores leave records in MongoDB `leaves` collection
   - Triggers risk analysis automatically

3. **Risk Analysis**:
   - Fetches all Jira tasks from database
   - For each task with assignee_email and due date:
     - Checks if assignee has leave overlapping with task due date
     - If overlap found, creates risk alert
   - Stores risk alerts in MongoDB `risk_alerts` collection

4. **Risk Alerts**:
   - Accessible via `/api/risks` endpoint
   - Shows task key, title, assignee, due date, leave dates
   - Status: OPEN/CLOSED
   - Risk level: HIGH

## Testing Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Prepare Test Data

**Create test leave file (leaves.csv):**
```csv
employee_email,leave_start,leave_end
john.doe@company.com,2025-12-20,2025-12-25
jane.smith@company.com,2026-01-05,2026-01-10
```

### 3. Test Flow

1. Start the backend server:
   ```bash
   python start_server.py
   ```

2. Login to the application

3. Connect to Jira (if not already connected)

4. Sync Jira data to get tasks with assignee emails

5. Upload the leave file via Data Management page

6. Check the file status - should show "processed"

7. Check risk alerts:
   ```bash
   GET /api/risks
   ```

8. You should see risk alerts for any tasks where:
   - Task has a due date
   - Task assignee email matches leave record
   - Due date falls within leave period

## API Endpoints

### Upload Leave File
```
POST /api/files/upload
Content-Type: multipart/form-data
Body: file (Excel/CSV)
```

### Get Risk Alerts
```
GET /api/risks
Response: Array of risk alerts
```

### Trigger Manual Risk Analysis
```
GET /api/risks/check
Response: { message, new_risks_created, data }
```

## Database Schema

### Leaves Collection
```javascript
{
  employee_email: "john.doe@company.com",
  leave_start: Date(2025-12-20),
  leave_end: Date(2025-12-25),
  file_id: ObjectId,
  uploaded_at: ISODate
}
```

### Risk Alerts Collection
```javascript
{
  task_key: "PROJ-123",
  task_title: "Implement feature X",
  assignee: "john.doe@company.com",
  due_date: Date(2025-12-22),
  leave_start: Date(2025-12-20),
  leave_end: Date(2025-12-25),
  risk_level: "HIGH",
  status: "OPEN",
  created_at: ISODate
}
```

### Jira Tasks Collection
```javascript
{
  user_id: "user123",
  key: "PROJ-123",
  summary: "Task summary",
  assignee: "John Doe",
  assignee_email: "john.doe@company.com",  // NEW FIELD
  duedate: ISODate(2025-12-22),
  status: "In Progress",
  priority: "High",
  // ... other fields
}
```

## Notes

- Leave files can be Excel (.xlsx, .xls) or CSV (.csv)
- Employee emails in leave files are automatically converted to lowercase for matching
- Risk analysis runs automatically after leave file processing
- Risk analysis can also be triggered manually via `/api/risks/check`
- Only creates risk alerts if task has both assignee_email and due date
- Duplicate risk alerts are prevented (checks for existing OPEN risks for the same task)
