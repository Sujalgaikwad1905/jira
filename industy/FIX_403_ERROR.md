# 🔧 403 Forbidden Error - SOLUTION

## Problem
Getting 403 Forbidden error on `/api/dashboard/stats` and other APIs even after login.

## Root Cause Analysis

Looking at your logs:
```
✅ GET /api/dashboard/ - 200 OK  (works)
✅ GET /api/risks/check - 200 OK  (works)
❌ GET /api/dashboard/stats - 403 Forbidden  (fails)
```

The **403 Forbidden** error means:
- ✅ You ARE authenticated (token is valid)
- ❌ You DON'T have permission (likely email not verified)

## Most Likely Cause: EMAIL NOT VERIFIED

The dashboard routes use `get_current_user` which allows unverified users, BUT some specific endpoints or the dashboard service itself might be checking verification status.

## Solution Steps

### Step 1: Check User Verification Status
```bash
cd d:\working\industy\backend
python verify_user.py list
```

This will show all users and their verification status:
```
======================================================================
ALL USERS IN DATABASE
======================================================================

1. ❌ user@example.com
   Name: John Doe
   Verified: False  ← THIS IS THE PROBLEM
   Role: user
```

### Step 2: Manually Verify Your User
```bash
python verify_user.py your-email@example.com
```

Example:
```bash
python verify_user.py user@example.com
```

Expected output:
```
📧 User: user@example.com
   Name: John Doe
   Verified: False
   Role: user

✅ Successfully verified user: user@example.com
```

### Step 3: Restart Backend & Test
```bash
# Stop backend (Ctrl+C)
python start_server.py
```

### Step 4: Clear Browser & Re-login
```javascript
// In browser console (F12)
localStorage.clear();
location.reload();
```

Then login again. Now all APIs should work!

## Alternative: Verify Via MongoDB Directly

If you have MongoDB Compass or CLI:

```javascript
// In MongoDB shell or Compass
use multidesk;

// Find your user
db.users.find({ email: "your-email@example.com" });

// Verify user
db.users.updateOne(
  { email: "your-email@example.com" },
  { $set: { is_verified: true } }
);
```

## Why This Happened

During registration:
1. User account created with `is_verified: false`
2. Email with OTP should be sent
3. User should verify email with OTP
4. System sets `is_verified: true`

If email service isn't configured or you skipped verification:
- User can login (gets token)
- But some APIs require verified status
- Results in 403 Forbidden

## Enhanced Logging Added

The backend now logs verification status:

**When checking authentication:**
```
🔐 Attempting to verify token: eyJhbGci...
✓ Token verified for email: user@example.com
✅ User authenticated: user@example.com (verified: false)
```

**When checking verification:**
```
📝 Checking verification status for: user@example.com
⚠️ User user@example.com is NOT VERIFIED - returning 403
```

## Permanent Fix Options

### Option 1: Auto-Verify Users (Development Only)
For development, you can auto-verify users on registration:

**File:** `backend/services/auth_service.py`
```python
# In create_user method, change:
"is_verified": False,
# To:
"is_verified": True,  # Auto-verify in development
```

### Option 2: Skip Email Verification (Development Only)
Remove verification requirement from protected routes.

### Option 3: Setup Email Service (Production)
Configure email service properly so OTP verification works:

**File:** `backend/.env`
```bash
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USER=your-email@gmail.com
MAIL_PASS=your-app-password
MAIL_FROM=your-email@gmail.com
```

## Verification Checklist

After running the verify script:

- [ ] Run `python verify_user.py list` - shows verified: True
- [ ] Restart backend server
- [ ] Clear browser localStorage
- [ ] Login again
- [ ] Test dashboard stats API - should return 200 OK
- [ ] Check backend logs - should show "verified: true"

## Quick Test Command

After verification, test the API:

```bash
# Get your token from browser localStorage
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/dashboard/stats
```

Should return JSON data instead of 403.

## Summary

**The Issue:** User email not verified (`is_verified: false`)  
**The Fix:** Run `python verify_user.py your-email@example.com`  
**Result:** 403 → 200 OK ✅

---

**Files Created:**
- `verify_user.py` - Script to verify users manually
- Enhanced logging in `dependencies.py` for better debugging
