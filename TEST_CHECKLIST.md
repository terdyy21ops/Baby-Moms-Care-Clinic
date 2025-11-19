# User Management Testing Checklist

## Pre-Testing Setup

### 1. Ensure Server is Running
```bash
python manage.py runserver
```

### 2. Create Test Users (if needed)
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile

# Create test mother
mother = User.objects.create_user('test_mother', 'mother@test.com', 'testpass123')
mother.first_name = 'Jane'
mother.last_name = 'Doe'
mother.save()
UserProfile.objects.create(user=mother, role='mother', phone='1234567890')

# Create test doctor
doctor = User.objects.create_user('test_doctor', 'doctor@test.com', 'testpass123')
doctor.first_name = 'Dr. John'
doctor.last_name = 'Smith'
doctor.save()
UserProfile.objects.create(user=doctor, role='doctor', phone='0987654321')

print("Test users created successfully!")
```

---

## Testing Checklist

### ✅ Test 1: Access Control
**Objective**: Verify only admins can access user management

- [ ] **Step 1**: Log out if logged in
- [ ] **Step 2**: Log in as Mother (test_mother / testpass123)
- [ ] **Step 3**: Try to access: `http://127.0.0.1:8000/accounts/users/`
- [ ] **Expected**: Redirected to dashboard with error message
- [ ] **Step 4**: Log out
- [ ] **Step 5**: Log in as Admin
- [ ] **Step 6**: Access: `http://127.0.0.1:8000/accounts/users/`
- [ ] **Expected**: User management page loads successfully

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 2: View User List
**Objective**: Verify all users are displayed correctly

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to: `http://127.0.0.1:8000/accounts/users/`
- [ ] **Step 3**: Verify table shows:
  - [ ] Username column
  - [ ] Full Name column
  - [ ] Email column
  - [ ] Role column (with colored badges)
  - [ ] Status column (Active/Deactivated)
  - [ ] Last Login column
  - [ ] Actions column (Edit, Toggle, Delete icons)
- [ ] **Step 4**: Verify at least 3 users are visible
- [ ] **Expected**: All users displayed with correct information

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 3: Filter by Role
**Objective**: Verify role filter works correctly

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Select "Mother" from Role dropdown
- [ ] **Step 3**: Click "Apply Filters"
- [ ] **Expected**: Only users with Mother role displayed
- [ ] **Step 4**: Select "Doctor" from Role dropdown
- [ ] **Step 5**: Click "Apply Filters"
- [ ] **Expected**: Only users with Doctor role displayed
- [ ] **Step 6**: Click "Clear" button
- [ ] **Expected**: All users displayed again

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 4: Filter by Status
**Objective**: Verify status filter works correctly

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Select "Active" from Status dropdown
- [ ] **Step 3**: Click "Apply Filters"
- [ ] **Expected**: Only active users displayed
- [ ] **Step 4**: Select "Deactivated" from Status dropdown
- [ ] **Step 5**: Click "Apply Filters"
- [ ] **Expected**: Only deactivated users displayed (may be empty)
- [ ] **Step 6**: Click "Clear" button
- [ ] **Expected**: All users displayed again

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 5: Edit User
**Objective**: Verify user editing works correctly

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Click ✏️ (Edit) icon for test_mother
- [ ] **Expected**: Edit page loads with user information
- [ ] **Step 3**: Change first name to "Janet"
- [ ] **Step 4**: Change phone to "5555555555"
- [ ] **Step 5**: Click "Save Changes"
- [ ] **Expected**: Redirected to user management with success message
- [ ] **Step 6**: Verify changes are reflected in the table
- [ ] **Expected**: First name shows "Janet" and phone updated

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 6: Deactivate User
**Objective**: Verify user deactivation works correctly

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Note the status of test_mother (should be Active)
- [ ] **Step 3**: Click 🔄 (Toggle Status) icon for test_mother
- [ ] **Expected**: JavaScript confirmation dialog appears
- [ ] **Step 4**: Click "OK" to confirm
- [ ] **Expected**: Redirected with success message
- [ ] **Step 5**: Verify test_mother status changed to "✗ Deactivated"
- [ ] **Expected**: Status badge is red with "Deactivated" text

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 7: Login Block for Deactivated User
**Objective**: Verify deactivated users cannot log in

- [ ] **Step 1**: Log out from admin account
- [ ] **Step 2**: Go to login page: `http://127.0.0.1:8000/accounts/login/`
- [ ] **Step 3**: Try to log in as test_mother (testpass123)
- [ ] **Expected**: Login fails with error message
- [ ] **Step 4**: Verify error message says: "Your account has been deactivated. Please contact support."
- [ ] **Expected**: User remains on login page, not logged in

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 8: Reactivate User
**Objective**: Verify user reactivation works correctly

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to user management page
- [ ] **Step 3**: Filter by Status: "Deactivated"
- [ ] **Step 4**: Find test_mother (should be deactivated)
- [ ] **Step 5**: Click 🔄 (Toggle Status) icon
- [ ] **Expected**: JavaScript confirmation dialog appears
- [ ] **Step 6**: Click "OK" to confirm
- [ ] **Expected**: Redirected with success message
- [ ] **Step 7**: Verify test_mother status changed to "✓ Active"
- [ ] **Expected**: Status badge is green with "Active" text

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 9: Login After Reactivation
**Objective**: Verify reactivated users can log in

- [ ] **Step 1**: Log out from admin account
- [ ] **Step 2**: Go to login page
- [ ] **Step 3**: Log in as test_mother (testpass123)
- [ ] **Expected**: Login successful
- [ ] **Step 4**: Verify redirected to dashboard
- [ ] **Expected**: Dashboard loads with mother's view

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 10: Self-Protection (Deactivate)
**Objective**: Verify admin cannot deactivate themselves

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to user management page
- [ ] **Step 3**: Find your own admin account in the list
- [ ] **Step 4**: Try to click 🔄 (Toggle Status) icon
- [ ] **Expected**: Either icon is disabled OR error message appears
- [ ] **Step 5**: If action was attempted, verify error: "You cannot deactivate your own account."
- [ ] **Expected**: Admin account remains active

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 11: Delete User Confirmation
**Objective**: Verify delete confirmation page works

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Click 🗑️ (Delete) icon for test_doctor
- [ ] **Expected**: Delete confirmation page loads
- [ ] **Step 3**: Verify warning message is displayed
- [ ] **Step 4**: Verify user details are shown (username, name, email, role)
- [ ] **Step 5**: Click "Cancel" button
- [ ] **Expected**: Redirected back to user management
- [ ] **Step 6**: Verify test_doctor still exists in the list

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 12: Delete User
**Objective**: Verify user deletion works correctly

- [ ] **Step 1**: On user management page
- [ ] **Step 2**: Click 🗑️ (Delete) icon for test_doctor
- [ ] **Step 3**: On confirmation page, click "Yes, Delete User"
- [ ] **Expected**: Redirected to user management with success message
- [ ] **Step 4**: Verify test_doctor no longer appears in the list
- [ ] **Step 5**: Try to log in as test_doctor
- [ ] **Expected**: Login fails (user doesn't exist)

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 13: Self-Protection (Delete)
**Objective**: Verify admin cannot delete themselves

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to user management page
- [ ] **Step 3**: Find your own admin account
- [ ] **Step 4**: Try to click 🗑️ (Delete) icon
- [ ] **Expected**: Either icon is disabled OR error message appears
- [ ] **Step 5**: If action was attempted, verify error: "You cannot delete your own account."
- [ ] **Expected**: Admin account still exists

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 14: Django Admin Integration
**Objective**: Verify Django admin enhancements work

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to: `http://127.0.0.1:8000/admin/`
- [ ] **Step 3**: Click on "Users" under Authentication
- [ ] **Step 4**: Verify "Account Status" column is visible
- [ ] **Step 5**: Verify status shows "✓ Active" or "✗ Deactivated"
- [ ] **Step 6**: Select 2-3 active users (checkboxes)
- [ ] **Step 7**: Select "Deactivate selected users" from Action dropdown
- [ ] **Step 8**: Click "Go" button
- [ ] **Expected**: Success message appears
- [ ] **Step 9**: Verify selected users now show "✗ Deactivated"
- [ ] **Step 10**: Select the same users again
- [ ] **Step 11**: Select "Activate selected users" from Action dropdown
- [ ] **Step 12**: Click "Go" button
- [ ] **Expected**: Users reactivated successfully

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 15: Dashboard Link
**Objective**: Verify user management link in admin dashboard

- [ ] **Step 1**: Log in as Admin
- [ ] **Step 2**: Go to dashboard: `http://127.0.0.1:8000/accounts/dashboard/`
- [ ] **Step 3**: Look for "User Management" card in Quick Actions
- [ ] **Step 4**: Click on "User Management" card
- [ ] **Expected**: Redirected to user management page
- [ ] **Step 5**: Verify page loads correctly

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 16: Responsive Design
**Objective**: Verify pages work on different screen sizes

- [ ] **Step 1**: Open user management page
- [ ] **Step 2**: Resize browser to mobile size (375px width)
- [ ] **Expected**: Table scrolls horizontally or adapts to mobile
- [ ] **Step 3**: Verify filters are still accessible
- [ ] **Step 4**: Verify action buttons are still clickable
- [ ] **Step 5**: Resize to tablet size (768px width)
- [ ] **Expected**: Layout adjusts appropriately
- [ ] **Step 6**: Resize to desktop size (1920px width)
- [ ] **Expected**: Full layout displays correctly

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 17: Error Handling
**Objective**: Verify error handling works correctly

- [ ] **Step 1**: Try to access non-existent user edit page
  - URL: `http://127.0.0.1:8000/accounts/users/99999/edit/`
- [ ] **Expected**: 404 error or appropriate error message
- [ ] **Step 2**: Try to toggle status of non-existent user
  - URL: `http://127.0.0.1:8000/accounts/users/99999/toggle-status/`
- [ ] **Expected**: 404 error or appropriate error message
- [ ] **Step 3**: Try to delete non-existent user
  - URL: `http://127.0.0.1:8000/accounts/users/99999/delete/`
- [ ] **Expected**: 404 error or appropriate error message

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 18: Database Integrity
**Objective**: Verify database changes are correct

- [ ] **Step 1**: Open Django shell: `python manage.py shell`
- [ ] **Step 2**: Run:
```python
from apps.accounts.models import UserProfile
from django.contrib.auth.models import User

# Check account_status field exists
profile = UserProfile.objects.first()
print(f"Account Status: {profile.account_status}")
print(f"Is Active: {profile.is_account_active()}")

# Check deactivated user
user = User.objects.get(username='test_mother')
print(f"User is_active: {user.is_active}")
print(f"Profile status: {user.userprofile.account_status}")
```
- [ ] **Expected**: No errors, fields exist and have correct values

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 19: Migration Status
**Objective**: Verify migration was applied correctly

- [ ] **Step 1**: Run: `python manage.py showmigrations accounts`
- [ ] **Expected**: See `[X] 0002_userprofile_account_status`
- [ ] **Step 2**: Run: `python manage.py check`
- [ ] **Expected**: "System check identified no issues (0 silenced)."

**Status**: ⬜ Pass / ⬜ Fail

---

### ✅ Test 20: Performance
**Objective**: Verify page loads quickly

- [ ] **Step 1**: Clear browser cache
- [ ] **Step 2**: Load user management page
- [ ] **Step 3**: Note load time (should be < 2 seconds)
- [ ] **Step 4**: Apply filters multiple times
- [ ] **Expected**: Filters respond quickly (< 1 second)
- [ ] **Step 5**: Edit user and save
- [ ] **Expected**: Save completes quickly (< 2 seconds)

**Status**: ⬜ Pass / ⬜ Fail

---

## Summary

### Test Results
- Total Tests: 20
- Passed: ___
- Failed: ___
- Pass Rate: ___%

### Issues Found
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Notes
_______________________________________________
_______________________________________________
_______________________________________________

### Tested By
- Name: _______________________________________________
- Date: _______________________________________________
- Environment: _______________________________________________

---

## Quick Test Commands

```bash
# Check for errors
python manage.py check

# View migrations
python manage.py showmigrations accounts

# Run server
python manage.py runserver

# Access Django shell
python manage.py shell

# Create superuser (if needed)
python manage.py createsuperuser
```

---

## Cleanup After Testing

```python
# In Django shell
from django.contrib.auth.models import User

# Delete test users
User.objects.filter(username='test_mother').delete()
User.objects.filter(username='test_doctor').delete()

print("Test users deleted!")
```

---

**Testing Complete!** ✅

If all tests pass, the user management system is ready for production use.
