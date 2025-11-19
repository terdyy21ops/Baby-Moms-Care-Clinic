# User Management Enhancement Guide

## Overview
This enhancement adds comprehensive user management features to the Baby Moms Care Django Admin system, allowing administrators to manage user accounts effectively.

## Features Implemented

### 1. Account Status Management
- **New Field**: `account_status` added to `UserProfile` model
  - Options: `active` or `deactivated`
  - Default: `active`
- **Deactivated users cannot log in** - blocked at authentication level
- **Admin can toggle status** with one click

### 2. User Management Page (`/accounts/users/`)
**Access**: Admin role only

**Features**:
- View all users in a table format
- Display: Username, Full Name, Email, Role, Status, Last Login
- **Filters**:
  - Filter by Role (Mother, Doctor, Admin)
  - Filter by Status (Active, Deactivated)
- **Actions per user**:
  - ✏️ Edit - Modify user details
  - 🔄 Toggle Status - Activate/Deactivate account
  - 🗑️ Delete - Remove user permanently

### 3. Edit User Page
- Admin can update:
  - First Name, Last Name
  - Email
  - Role (Mother, Doctor, Admin)
  - Phone Number
- Displays account information (username, status, join date, last login)

### 4. Delete User Page
- Confirmation page with warning
- Shows user details before deletion
- Prevents accidental deletions
- **Note**: Admin cannot delete their own account

### 5. Enhanced Django Admin
**New Features**:
- Display account status in user list
- Bulk actions:
  - "Activate selected users"
  - "Deactivate selected users"
- Additional filters for account status

### 6. Security Features
- Deactivated users blocked at login
- Error message: "Your account has been deactivated. Please contact support."
- Admin cannot deactivate/delete themselves
- Role-based access control (only admins can access user management)

## Files Modified

### Models (`apps/accounts/models.py`)
```python
# Added fields:
- account_status (CharField with choices)
- is_account_active() method
```

### Views (`apps/accounts/views.py`)
```python
# Added views:
- user_management_view() - List all users
- toggle_user_status() - Activate/Deactivate users
- edit_user_view() - Edit user details
- delete_user_view() - Delete users

# Modified:
- CustomLoginView.form_valid() - Block deactivated users
```

### Forms (`apps/accounts/forms.py`)
```python
# Added:
- AdminUserEditForm - Form for editing users
```

### URLs (`apps/accounts/urls.py`)
```python
# Added routes:
- /accounts/users/ - User management page
- /accounts/users/<id>/toggle-status/ - Toggle status
- /accounts/users/<id>/edit/ - Edit user
- /accounts/users/<id>/delete/ - Delete user
```

### Admin (`apps/accounts/admin.py`)
```python
# Enhanced:
- Added account_status to list display
- Added bulk activate/deactivate actions
- Added status filter
```

### Templates Created
1. `templates/accounts/user_management.html` - Main user list
2. `templates/accounts/edit_user.html` - Edit user form
3. `templates/accounts/delete_user.html` - Delete confirmation

## Usage Instructions

### For Admins

#### Access User Management
1. Log in as admin
2. Go to Dashboard
3. Click "User Management" card
4. Or navigate to: `/accounts/users/`

#### Deactivate a User
1. Go to User Management page
2. Find the user in the table
3. Click the 🔄 icon (user-x)
4. Confirm the action
5. User will be logged out and cannot log in again

#### Reactivate a User
1. Go to User Management page
2. Filter by Status: "Deactivated" (optional)
3. Find the user
4. Click the 🔄 icon (user-check)
5. User can now log in again

#### Edit User Details
1. Go to User Management page
2. Click the ✏️ icon next to the user
3. Update the information
4. Click "Save Changes"

#### Delete a User
1. Go to User Management page
2. Click the 🗑️ icon next to the user
3. Review the warning and user details
4. Click "Yes, Delete User" to confirm
5. **Warning**: This action cannot be undone!

#### Use Filters
- **By Role**: Select Mother/Doctor/Admin from dropdown
- **By Status**: Select Active/Deactivated from dropdown
- Click "Apply Filters"
- Click "Clear" to reset filters

### For Deactivated Users
When a deactivated user tries to log in:
1. They enter credentials
2. System shows error: "Your account has been deactivated. Please contact support."
3. They cannot access the system
4. They must contact admin for reactivation

## Database Changes

### Migration Applied
```bash
python manage.py makemigrations accounts
python manage.py migrate accounts
```

**Migration**: `0002_userprofile_account_status.py`
- Adds `account_status` field to `userprofile` table
- Default value: `'active'`
- All existing users automatically set to `'active'`

## Security Considerations

1. **Role-Based Access**: Only admins can access user management
2. **Self-Protection**: Admins cannot deactivate/delete themselves
3. **Login Blocking**: Deactivated users blocked at authentication level
4. **Confirmation Dialogs**: JavaScript confirms for status changes and deletions
5. **Audit Trail**: User actions logged through Django messages

## Testing Checklist

- [ ] Admin can view user management page
- [ ] Non-admin users redirected from user management
- [ ] Filters work correctly (role and status)
- [ ] Edit user updates information correctly
- [ ] Toggle status changes user status
- [ ] Deactivated users cannot log in
- [ ] Reactivated users can log in
- [ ] Delete user removes user from database
- [ ] Admin cannot deactivate themselves
- [ ] Admin cannot delete themselves
- [ ] Django admin bulk actions work
- [ ] Migration applied successfully

## Troubleshooting

### Issue: Migration Error
**Solution**: Run migrations manually:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Deactivated User Can Still Log In
**Solution**: Check that:
1. Migration was applied
2. `account_status` field exists in database
3. User's `is_active` field is set to `False`

### Issue: Admin Cannot Access User Management
**Solution**: Verify:
1. User has `UserProfile` with `role='admin'`
2. User is logged in
3. URL is correct: `/accounts/users/`

## Future Enhancements (Optional)

1. **Email Notifications**: Notify users when deactivated/reactivated
2. **Deactivation Reason**: Add field to track why user was deactivated
3. **Temporary Deactivation**: Set expiration date for deactivation
4. **Activity Log**: Track all admin actions on users
5. **Bulk Operations**: Select multiple users for batch operations
6. **Export Users**: Download user list as CSV/Excel
7. **Advanced Search**: Search by username, email, name

## Support

For issues or questions:
- Check this guide first
- Review Django error logs
- Contact system administrator

---

**Version**: 1.0  
**Last Updated**: 2024  
**Compatible With**: Django 5.0.7+
