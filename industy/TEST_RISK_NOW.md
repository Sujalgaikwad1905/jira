# 🔥 RISK DETECTION - READY TO TEST

## ✅ What's Fixed

1. **Enhanced Logging** - Shows exactly what's happening
2. **Email Normalization** - Strips and lowercases emails for matching
3. **Better Date Handling** - Proper datetime to date conversion
4. **Debug Info** - Shows why risks aren't created

## 🚀 Test Steps

### Step 1: Check What's in Database
```bash
cd d:\working\industy\backend
python check_data.py
```

This shows:
- How many Jira tasks exist
- What assignee_email values are in tasks
- How many leaves exist
- What email values are in leaves
- Current risk alerts

### Step 2: Trigger Risk Analysis
```bash
curl http://localhost:8000/api/risks/check
```

### Step 3: Check Backend Logs

You'll see detailed logs like:

**Good - Found overlap:**
```
🔍 Starting risk analysis...
🔎 Checking PROJ-123 - Assignee: sujalgaikwadusa@gmail.com, Due: 2025-12-20
⚠️ OVERLAP FOUND for PROJ-123!
   Task due: 2025-12-20
   Leave: 2025-12-15 to 2025-12-31
✅ Created risk alert for PROJ-123 - sujalgaikwadusa@gmail.com on leave
📊 Analysis complete: 10 total tasks, 10 checked, 0 skipped
🚨 1 new risk alerts created
```

**If no overlap:**
```
🔎 Checking PROJ-123 - Assignee: sujalgaikwadusa@gmail.com, Due: 2025-01-05
   No overlap found. User has 1 leave records total
```

**If no assignee_email:**
```
❌ Skipping PROJ-456: No assignee_email
```

## 🔍 Debug Commands

**Check specific user's leaves:**
```bash
# In MongoDB Compass or shell
db.leaves.find({ employee_email: "sujalgaikwadusa@gmail.com" })
```

**Check specific user's tasks:**
```bash
db.jira_tasks.find({ assignee_email: "sujalgaikwadusa@gmail.com" })
```

**Check all risks:**
```bash
curl http://localhost:8000/api/risks
```

## 📋 Common Issues & Solutions

### Issue: "No overlap found"
**Check:**
1. Task has `assignee_email` field (not just `assignee`)
2. Leave email matches task email exactly
3. Task `duedate` falls within leave dates

**Fix:** 
- Re-sync Jira to get assignee_email
- Or manually add assignee_email to existing tasks

### Issue: "No assignee_email"
**Means:** Jira tasks don't have email, only display name

**Fix:**
```javascript
// Add assignee_email to test task in MongoDB
db.jira_tasks.updateOne(
  { key: "PROJ-123" },
  { $set: { assignee_email: "sujalgaikwadusa@gmail.com" } }
)
```

### Issue: "User has 0 leave records"
**Means:** Leave wasn't saved or email doesn't match

**Check:**
```bash
db.leaves.find({})  // See all leaves
```

## ✅ Success Check

Risk should be created if:
- ✅ Task has `assignee_email` field
- ✅ Task has `duedate` field
- ✅ Leave has matching `employee_email`
- ✅ Task duedate is between leave_start and leave_end

Example:
- Task: assignee_email="sujalgaikwadusa@gmail.com", duedate=2025-12-20
- Leave: employee_email="sujalgaikwadusa@gmail.com", start=2025-12-15, end=2025-12-31
- Result: ✅ RISK CREATED!

## 🎯 Quick Test

1. Run `python check_data.py` - See what's in DB
2. Hit `/api/risks/check` - Trigger analysis
3. Check logs - See detailed processing
4. Hit `/api/risks` - See created alerts

The logs will tell you EXACTLY why risks are or aren't being created!
