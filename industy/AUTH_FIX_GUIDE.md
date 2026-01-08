# 🔐 Authentication Issue - Fix Guide

## Issues Fixed

### 1. **Missing CORS Origin for Vite Dev Server**
**Problem:** Frontend running on `http://localhost:5173` (Vite default) was not in allowed CORS origins.

**Fix:** Added Vite's default port to CORS configuration in `main.py`
```python
allow_origins=[
    "http://localhost:5173",  # Vite dev server ✨ ADDED
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000"
]
```

### 2. **Poor Error Logging**
**Problem:** No visibility into why authentication was failing.

**Fix:** Added detailed logging in:
- `utils/dependencies.py` - Logs token verification steps
- `services/auth_service.py` - Logs JWT decode errors, expired tokens

### 3. **Token Storage**
**Verified:** Frontend properly stores and sends tokens via:
- LocalStorage: `access_token` key
- Authorization header: `Bearer <token>`

## 🔍 Troubleshooting Steps

### Step 1: Test Authentication Locally
```bash
cd d:\working\industy\backend
python test_auth.py
```

**Expected Output:**
```
==================================================
Testing Authentication Flow
==================================================

1. Creating test token...
✓ Token created: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

2. Verifying token...
✓ Token verified successfully for: test@example.com

3. Checking configuration...
Secret Key: your-secret-key-cha...
Algorithm: HS256
Token Expire: 30 minutes

==================================================
✓ All authentication tests passed!
==================================================
```

### Step 2: Check Browser Developer Tools

#### A. Check if token is stored
1. Open browser DevTools (F12)
2. Go to **Application** tab → **Local Storage**
3. Look for `http://localhost:5173`
4. Verify `access_token` key exists with a long JWT string

#### B. Check API requests
1. Go to **Network** tab
2. Make a protected API call
3. Click on the request
4. Check **Request Headers**:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

#### C. Check response
- **200 OK** = Authentication working ✅
- **401 Unauthorized** = Authentication failed ❌
  - Check response for error details

### Step 3: Check Backend Logs

Start the backend with logging:
```bash
cd d:\working\industy\backend
python start_server.py
```

**Look for these log messages:**

✅ **Successful Authentication:**
```
DEBUG - Attempting to verify token: eyJhbGciOiJIUzI1NiIs...
DEBUG - Token verified successfully for: user@example.com
DEBUG - Token verified for email: user@example.com
DEBUG - User authenticated: user@example.com
```

❌ **Failed Authentication:**
```
WARNING - Token verification failed: invalid token data
WARNING - JWT verification failed: Signature has expired
WARNING - User not found for email: user@example.com
```

### Step 4: Common Issues & Fixes

#### Issue 1: "Could not validate credentials"
**Possible Causes:**
1. Token expired (30 min default)
2. Token not sent in header
3. Wrong secret key
4. User logged in on old backend, new secret key generated

**Solution:**
1. Log out and log in again
2. Check browser local storage for token
3. Verify SECRET_KEY in `.env` hasn't changed
4. Clear browser local storage and re-login

#### Issue 2: CORS Error
**Error:** `Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:5173' has been blocked by CORS policy`

**Solution:**
- ✅ Already fixed! CORS now includes localhost:5173
- Restart backend server if it was running

#### Issue 3: Token Expired
**Error:** `JWT verification failed: Signature has expired`

**Solution:**
```javascript
// In browser console
localStorage.removeItem('access_token');
localStorage.removeItem('user_data');
// Then log in again
```

#### Issue 4: 401 on all requests even after login
**Debug:**
```javascript
// In browser console
console.log('Token:', localStorage.getItem('access_token'));
console.log('User:', localStorage.getItem('user_data'));
```

**If null:**
- Login flow not storing token
- Check login API response in Network tab

**If token exists:**
- Backend not accepting token
- Check backend logs
- Run `python test_auth.py` to verify JWT is working

## 🚀 Quick Fix Checklist

- [x] CORS configuration updated with localhost:5173
- [x] Logging added to authentication flow
- [x] Test script created (test_auth.py)
- [ ] Restart backend server
- [ ] Clear browser cache and local storage
- [ ] Log in again
- [ ] Check backend logs for errors

## 📋 Files Modified

1. **backend/main.py**
   - Added Vite dev server to CORS origins
   
2. **backend/utils/dependencies.py**
   - Added detailed logging for token verification
   - Better error messages
   
3. **backend/services/auth_service.py**
   - Added logging for JWT operations
   - Separate handling for expired tokens

4. **backend/test_auth.py** (NEW)
   - Test script to verify JWT is working

## 🔧 Test the Fix

### 1. Restart Backend
```bash
cd d:\working\industy\backend
# Stop current server (Ctrl+C)
python start_server.py
```

### 2. Clear Frontend Storage
```javascript
// In browser console (F12)
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### 3. Login Again
1. Go to http://localhost:5173
2. Login with your credentials
3. Check Network tab - login should return token
4. Navigate to protected page (Dashboard, Tasks, etc.)
5. Check Network tab - requests should have Authorization header

### 4. Verify in Backend Logs
Look for:
```
DEBUG - Attempting to verify token: eyJhbGci...
DEBUG - Token verified successfully for: your@email.com
DEBUG - User authenticated: your@email.com
```

## 🆘 If Still Not Working

### Enable Debug Logging

**Backend (.env):**
```bash
# Add to .env
LOG_LEVEL=DEBUG
```

**Start backend:**
```bash
python start_server.py
```

### Check Token Manually

**In browser console:**
```javascript
// Get your token
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// Decode token (just to see content, not verify)
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Token Payload:', payload);
console.log('Email:', payload.sub);
console.log('Expires:', new Date(payload.exp * 1000));
```

### Manual API Test

**Using curl:**
```bash
# Get your token from browser
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     http://localhost:8000/api/auth/me
```

**Using Postman:**
1. Create new request: GET http://localhost:8000/api/auth/me
2. Go to Authorization tab
3. Type: Bearer Token
4. Token: paste your token from localStorage
5. Send

## ✅ Expected Behavior After Fix

1. **Login:**
   - Token stored in localStorage
   - Redirected to dashboard

2. **Protected Routes:**
   - All API calls include Authorization header
   - Backend logs show token verification
   - No 401 errors

3. **Token Expiry:**
   - After 30 minutes, token expires
   - User gets 401 error
   - Frontend should redirect to login (implement this if not done)

## 📝 Next Steps

If you want to implement auto-refresh or better token handling:

1. **Add token refresh endpoint**
2. **Implement axios/fetch interceptor** to catch 401 and redirect
3. **Add token expiry check** before requests
4. **Implement refresh token flow** (more secure)

For now, users need to re-login after 30 minutes.
