# User Management - Quick Reference Card

## 🚀 Access User Management
```
URL: http://127.0.0.1:8000/accounts/users/
Access: Admin role only
```

## 🔑 Key Features

### 1️⃣ Deactivate User
```
Action: Click 🔄 icon (user-x) next to active user
Result: User cannot log in
Message: "Your account has been deactivated. Please contact support."
```

### 2️⃣ Reactivate User
```
Action: Click 🔄 icon (user-check) next to deactivated user
Result: User can log in again
```

### 3️⃣ Edit User
```
Action: Click ✏️ icon
Fields: First Name, Last Name, Email, Role, Phone
```

### 4️⃣ Delete User
```
Action: Click 🗑️ icon → Confirm
Warning: Cannot be undone!
```

## 🎯 URLs Added
```python
/accounts/users/                      # User management page
/accounts/users/<id>/toggle-status/   # Toggle active/deactivated
/accounts/users/<id>/edit/            # Edit user details
/accounts/users/<id>/delete/          # Delete user
```

## 🔒 Security Rules
- ✅ Only admins can access user management
- ✅ Deactivated users blocked at login
- ✅ Admin cannot deactivate themselves
- ✅ Admin cannot delete themselves

## 📊 Filters Available
```
Role: All | Mother | Doctor | Admin
Status: All | Active | Deactivated
```

## 🎨 Status Badges
```
✓ Active      → Green badge
✗ Deactivated → Red badge
```

## 🎭 Role Badges
```
Mother → Pink badge
Doctor → Blue badge
Admin  → Purple badge
```

## 🔧 Django Admin Actions
```
Location: /admin/auth/user/
Actions:
  - Activate selected users
  - Deactivate selected users
```

## 📝 Model Changes
```python
UserProfile.account_status
  - Choices: 'active', 'deactivated'
  - Default: 'active'

UserProfile.is_account_active()
  - Returns: True if active, False if deactivated
```

## 🧪 Quick Test
```bash
# 1. Run server
python manage.py runserver

# 2. Log in as admin
http://127.0.0.1:8000/accounts/login/

# 3. Go to user management
http://127.0.0.1:8000/accounts/users/

# 4. Test deactivate → Try login → Should fail
# 5. Test reactivate → Try login → Should work
```

## 🐛 Troubleshooting
```
Issue: Migration not applied
Fix: python manage.py migrate accounts

Issue: 404 on /accounts/users/
Fix: Check URL pattern in urls.py

Issue: Permission denied
Fix: Verify user has role='admin' in UserProfile

Issue: Deactivated user can still login
Fix: Check account_status field exists in database
```

## 📦 Files Modified
```
✏️ Modified (6):
  - apps/accounts/models.py
  - apps/accounts/views.py
  - apps/accounts/forms.py
  - apps/accounts/urls.py
  - apps/accounts/admin.py
  - templates/accounts/dashboard.html

➕ Created (4):
  - templates/accounts/user_management.html
  - templates/accounts/edit_user.html
  - templates/accounts/delete_user.html
  - migrations/0002_userprofile_account_status.py
```

## ⚡ Quick Commands
```bash
# Check for errors
python manage.py check

# View migrations
python manage.py showmigrations accounts

# Create superuser (if needed)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 💡 Pro Tips
1. Use filters to find users quickly
2. Deactivate instead of delete (safer)
3. Check last login to find inactive accounts
4. Use Django admin for bulk operations
5. Test with non-admin user to verify security

---
**Quick Access**: Dashboard → User Management Card
