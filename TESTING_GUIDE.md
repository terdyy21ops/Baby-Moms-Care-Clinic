# Appointment System Testing Guide

## ✅ Fixed Issues

1. **Appointments now save to database correctly**
2. **Patient is properly linked to logged-in mother**
3. **All appointment statuses are visible (Pending, Approved, Completed, Cancelled)**
4. **Appointment list loads without errors**
5. **Filtering and pagination work correctly**

## 🧪 How to Test

### Step 1: Login as Mother
1. Go to `http://127.0.0.1:8000/accounts/login/`
2. Login with a mother account
3. You should see the dashboard

### Step 2: Book an Appointment
1. Click "Appointments" in the navigation bar OR
2. Go directly to `http://127.0.0.1:8000/appointments/create/`
3. Fill out the form:
   - Select a doctor
   - Choose appointment type (e.g., "Consultation")
   - Pick a future date
   - Select a time (e.g., 10:00 AM)
   - Duration: 30 minutes (default)
   - Reason: Optional
4. Click "Book Appointment"

### Step 3: Verify Appointment Appears
1. You should be redirected to `http://127.0.0.1:8000/appointments/`
2. **Your appointment should appear immediately** in the list
3. Status should show as "Pending" (amber/yellow badge)
4. You should see:
   - Doctor's name
   - Date and time
   - Appointment type
   - Status badge
   - "View Details" button

### Step 4: Test Filtering
1. On the appointments page, use the status dropdown:
   - Select "Pending" - should show your new appointment
   - Select "Approved" - should show empty (until doctor approves)
   - Select "Completed" - should show empty
   - Select "Cancelled" - should show empty
   - Select "All Status" - should show all your appointments

### Step 5: Test Search
1. Type doctor's name in search box
2. Click "Filter"
3. Should show only appointments with that doctor

### Step 6: View Appointment Details
1. Click "View Details" on any appointment
2. Should show full appointment information:
   - Patient name (your name)
   - Doctor name
   - Date, time, duration
   - Status
   - Reason for visit
   - Options to cancel (if applicable)

### Step 7: Test as Doctor (Optional)
1. Logout and login as a doctor
2. Go to `http://127.0.0.1:8000/appointments/`
3. You should see the appointment the mother booked
4. Click "View Details"
5. You can approve/decline the appointment

### Step 8: Test as Admin (Optional)
1. Logout and login as admin
2. Go to `http://127.0.0.1:8000/appointments/`
3. You should see ALL appointments from all users
4. Can filter and search across all appointments

## 🔍 What to Check

### ✅ Appointment Creation
- [ ] Form loads without errors
- [ ] Can select doctor from dropdown
- [ ] Can pick date and time
- [ ] Form validates (no past dates, doctor availability)
- [ ] Success message appears after booking
- [ ] Redirects to appointments list

### ✅ Appointment List
- [ ] Page loads without errors
- [ ] Appointments appear immediately after booking
- [ ] Shows correct information (doctor, date, time, status)
- [ ] Status badges have correct colors:
  - Pending: Amber/Yellow
  - Approved: Green
  - Completed: Blue
  - Cancelled: Red
- [ ] "Book Appointment" button visible for mothers
- [ ] Empty state shows when no appointments

### ✅ Filtering
- [ ] Status filter works (pending, approved, completed, cancelled)
- [ ] Search works (by doctor name, reason)
- [ ] "All Status" shows all appointments
- [ ] Filters persist in URL

### ✅ Pagination
- [ ] Shows 10 appointments per page
- [ ] "Previous" and "Next" buttons work
- [ ] Page numbers display correctly

### ✅ Permissions
- [ ] Mothers only see their own appointments
- [ ] Doctors only see their own appointments
- [ ] Admins see all appointments
- [ ] Cannot view other users' appointment details

## 🐛 Common Issues & Solutions

### Issue: "No Appointments Found"
**Solution**: Make sure you're logged in as the same user who created the appointment.

### Issue: Form validation errors
**Solution**: 
- Check date is in the future
- Check time is during doctor's working hours (9 AM - 5 PM weekdays)
- Check doctor is selected

### Issue: "Doctor not available"
**Solution**: 
- Choose a weekday (Monday-Friday)
- Choose time between 9:00 AM - 5:00 PM
- Try a different time slot if one is taken

## 📊 Database Verification

To verify appointments are in the database:

```bash
python manage.py shell
```

Then run:
```python
from apps.appointments.models import Appointment
from django.contrib.auth.models import User

# Get a mother user
mother = User.objects.filter(userprofile__role='mother').first()
print(f"Mother: {mother.username}")

# Check their appointments
appointments = Appointment.objects.filter(patient=mother)
print(f"Total appointments: {appointments.count()}")

# Show details
for apt in appointments:
    print(f"- {apt.date} at {apt.time} with Dr. {apt.doctor.get_full_name()} - Status: {apt.status}")
```

## ✨ Expected Behavior

1. **After booking**: Appointment immediately appears in mother's list with "Pending" status
2. **Doctor approves**: Status changes to "Approved" (green badge)
3. **After appointment**: Doctor marks as "Completed" (blue badge)
4. **If cancelled**: Status shows "Cancelled" (red badge)

All appointments remain visible in the list regardless of status, unless filtered.

## 🎯 Success Criteria

✅ Mother can book appointment
✅ Appointment saves to database
✅ Appointment appears in "My Appointments" immediately
✅ All statuses are visible and filterable
✅ No errors in console or page
✅ Proper permissions enforced
✅ Notifications sent to doctor
