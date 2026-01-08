# 🔥 QUICK FIX - 2 STEPS TO MAKE IT WORK

## Problem Found:
1. ❌ Jira tasks have NO `assignee_email` field
2. ❌ Leave file didn't save to database (0 leaves)

## Solution:

### Step 1: Add Assignee Emails to Tasks
```bash
cd d:\working\industy\backend
python add_test_emails.py
```

This will:
- Add `assignee_email` to all 8 tasks
- Assign emails matching your test.csv file
- Show you which email was assigned to each task

### Step 2: Re-upload Your Leave File

**Stop and restart backend first:**
```bash
# Stop (Ctrl+C)
python start_server.py
```

**Then upload test.csv again:**
```bash
curl -X POST http://localhost:8000/api/files/upload \
  -F "file=@uploads/test.csv"
```

**OR in Postman:**
- POST `http://localhost:8000/api/files/upload`
- Body: form-data
- Key: `file`, Type: File
- Select: `uploads/test.csv`

### Step 3: Check Backend Logs

You should see:
```
📂 Processing leave file: uploads/test.csv
✅ File exists, size: 234 bytes
📊 File loaded: 6 rows, columns: ['employee_email', 'leave_start', 'leave_end']
✅ Required columns present
  Row 1: rahul@gmail.com from 2025-01-10 to 2025-01-12
  Row 2: priya@gmail.com from 2025-01-11 to 2025-01-11
  ...
✅ Inserted 6 leave records into database
```

### Step 4: Trigger Risk Analysis
```bash
curl http://localhost:8000/api/risks/check
```

### Step 5: Check Risks
```bash
curl http://localhost:8000/api/risks
```

## Expected Result:

After both steps:
- ✅ Tasks have assignee_email
- ✅ Leaves are in database
- ✅ Risk analysis finds matches
- ✅ Risk alerts created

## Quick Verify:

```bash
# Check again
python check_data.py
```

Should show:
- ✅ Tasks with assignee_email (not None)
- ✅ Leaves: 6 records
- ✅ Risks: X alerts (if dates overlap)

## Why This Happened:

1. **No assignee_email:** Jira sync didn't include emails (only display names)
2. **No leaves:** File upload worked but background task may have failed silently

## After Fix:

You'll see logs like:
```
⚠️ OVERLAP FOUND for SCRUM-7!
   Task due: 2025-12-31
   Leave: 2025-12-15 to 2025-12-31
✅ Created risk alert for SCRUM-7 - sujalgaikwadusa@gmail.com on leave
```

**Do steps 1 & 2 now and it will work!** 🚀
