# Doctor Features Testing Guide

## 🎯 Quick Test Scenario

### Scenario: Complete Doctor Workflow

#### Step 1: Mother Books Appointment
1. Login as mother
2. Go to Appointments → Book Appointment
3. Select doctor, date, time
4. Submit booking
5. Logout

#### Step 2: Doctor Sees New Appointment
1. Login as doctor
2. **VERIFY**: Automatically redirected to doctor dashboard
3. **VERIFY**: New appointment appears in "Today's Schedule" (if today) or "Upcoming Appointments"
4. **VERIFY**: "Pending Approval" count increased by 1
5. **VERIFY**: Status badge shows "Pending" in amber/yellow

#### Step 3: Doctor Approves Appointment
1. Click "Approve" button on the appointment
2. **VERIFY**: Status changes to "Approved" (green badge)
3. **VERIFY**: Success message appears
4. **VERIFY**: "Pending Approval" count decreased by 1
5. Logout and login as mother
6. **VERIFY**: Mother receives notification about approval

#### Step 4: Doctor Adds Medical Notes
1. Login as doctor
2. Click "View" on the approved appointment
3. Click "Add Medical Notes"
4. Fill in:
   - Diagnosis: "Routine prenatal checkup - healthy"
   - Prescription: "Prenatal vitamins - 1 tablet daily"
   - Follow-up: "Schedule next visit in 4 weeks"
5. Save
6. **VERIFY**: Medical information appears in appointment detail

#### Step 5: Doctor Marks as Complete
1. From appointment detail, click "Mark as Completed"
2. **VERIFY**: Status changes to "Completed" (blue badge)
3. **VERIFY**: "Completed Today" count increased by 1
4. **VERIFY**: Success message appears
5. Logout and login as mother
6. **VERIFY**: Mother receives completion notification
7. **VERIFY**: Mother can see medical notes in appointment detail

#### Step 6: Doctor Views Patient Records
1. Login as doctor
2. Open any appointment
3. Click "View Patient Records"
4. **VERIFY**: Shows all appointments with that patient
5. **VERIFY**: Shows patient profile information
6. **VERIFY**: Shows medical history

## 🔍 Detailed Feature Tests

### Test 1: Dashboard Visibility
**Expected**: All appointments appear regardless of status

1. Login as doctor
2. Check dashboard stats:
   - Today's Appointments: Shows count
   - Pending Approval: Shows count
   - Completed Today: Shows count
   - Total Patients: Shows count
3. Scroll to "Today's Schedule"
4. **VERIFY**: All today's appointments visible (pending, approved, completed)
5. Scroll to "Upcoming Appointments"
6. **VERIFY**: Future appointments visible

**Pass Criteria**: ✅ All appointments visible, stats accurate

### Test 2: Approve Appointment
**Expected**: Status changes, notification sent

1. Find pending appointment
2. Click "Approve"
3. **VERIFY**: Status → "Approved" (green)
4. **VERIFY**: Success message
5. **VERIFY**: Patient notified
6. **VERIFY**: "Approve" button no longer visible
7. **VERIFY**: "Complete" button now visible

**Pass Criteria**: ✅ Status updated, notification sent, UI updated

### Test 3: Decline Appointment
**Expected**: Status changes to cancelled

1. Find pending appointment
2. Click "Decline"
3. **VERIFY**: Status → "Cancelled" (red)
4. **VERIFY**: Success message
5. **VERIFY**: Patient notified
6. **VERIFY**: No action buttons visible

**Pass Criteria**: ✅ Status updated, notification sent

### Test 4: Mark as Complete
**Expected**: Approved appointment becomes completed

1. Find approved appointment
2. Click "Complete" (from dashboard or detail)
3. **VERIFY**: Status → "Completed" (blue)
4. **VERIFY**: Success message
5. **VERIFY**: Patient notified
6. **VERIFY**: "Complete" button no longer visible

**Pass Criteria**: ✅ Status updated, notification sent

### Test 5: Add Medical Notes
**Expected**: Medical information saved and displayed

1. Open approved appointment
2. Click "Add Medical Notes"
3. Fill all fields:
   - Diagnosis
   - Prescription
   - Follow-up Instructions
   - General Notes
4. Save
5. **VERIFY**: Redirected to detail page
6. **VERIFY**: All medical info displayed
7. **VERIFY**: Color-coded sections (blue, green, amber, gray)

**Pass Criteria**: ✅ All fields saved and displayed correctly

### Test 6: View Patient Records
**Expected**: Complete patient history visible

1. Open any appointment
2. Click "View Patient Records"
3. **VERIFY**: Patient name and profile shown
4. **VERIFY**: All appointments with this patient listed
5. **VERIFY**: Sorted by date (newest first)
6. **VERIFY**: Medical history visible

**Pass Criteria**: ✅ Complete patient history accessible

### Test 7: Appointment List Filtering
**Expected**: Can filter by status

1. Go to Appointments page
2. Select "Pending" from status dropdown
3. **VERIFY**: Only pending appointments shown
4. Select "Approved"
5. **VERIFY**: Only approved appointments shown
6. Select "Completed"
7. **VERIFY**: Only completed appointments shown
8. Select "All Status"
9. **VERIFY**: All appointments shown

**Pass Criteria**: ✅ Filtering works correctly

### Test 8: Search Functionality
**Expected**: Can search by patient name

1. Go to Appointments page
2. Type patient name in search box
3. Click "Filter"
4. **VERIFY**: Only matching appointments shown
5. Clear search
6. **VERIFY**: All appointments return

**Pass Criteria**: ✅ Search works correctly

## 🐛 Common Issues & Solutions

### Issue: "No Appointments Found"
**Solution**: 
- Verify you're logged in as doctor
- Check that mother has booked appointments
- Verify appointments are assigned to this doctor
- Check database: `Appointment.objects.filter(doctor=doctor_user)`

### Issue: Dashboard shows 0 appointments
**Solution**:
- Verify redirect is working (should go to `/appointments/doctor-dashboard/`)
- Check browser console for errors
- Verify appointments exist in database
- Check date filters (today's appointments only show today's date)

### Issue: Cannot approve/decline
**Solution**:
- Verify appointment status is "pending"
- Check user is the assigned doctor
- Verify URL routing is correct
- Check for JavaScript errors

### Issue: Medical notes not saving
**Solution**:
- Verify form is submitting (check POST request)
- Check for validation errors
- Verify user has permission (is the assigned doctor)
- Check database fields exist

## 📊 Expected Results Summary

| Action | Expected Result | Notification Sent |
|--------|----------------|-------------------|
| Mother books | Appears in doctor dashboard | ✅ To doctor |
| Doctor approves | Status → Approved (green) | ✅ To patient |
| Doctor declines | Status → Cancelled (red) | ✅ To patient |
| Doctor completes | Status → Completed (blue) | ✅ To patient |
| Add medical notes | Saved and displayed | ❌ No |
| View patient records | Shows history | ❌ No |

## ✅ Final Checklist

Before marking as complete, verify:

- [ ] Doctor login redirects to doctor dashboard
- [ ] All appointments visible (all statuses)
- [ ] Can approve pending appointments
- [ ] Can decline pending appointments
- [ ] Can mark approved as complete
- [ ] Can add medical notes (diagnosis, prescription, follow-up)
- [ ] Can view patient records
- [ ] All actions send notifications
- [ ] Status badges show correct colors
- [ ] Dashboard stats are accurate
- [ ] Filtering works (by status)
- [ ] Search works (by patient name)
- [ ] Rose pink theme consistent
- [ ] No console errors
- [ ] No database errors
- [ ] Mobile responsive

## 🎨 Visual Verification

### Status Badge Colors
- **Pending**: Amber background (#FEF3C7), Amber text (#92400E)
- **Approved**: Green background (#D1FAE5), Green text (#065F46)
- **Completed**: Blue background (#DBEAFE), Blue text (#1E40AF)
- **Cancelled**: Red background (#FEE2E2), Red text (#991B1B)

### Button Colors
- **Approve**: Green (#10B981)
- **Decline**: Red (#EF4444)
- **Complete**: Blue (#3B82F6)
- **View**: Rose Pink (#EC4899)
- **Edit**: Rose Pink (#EC4899)

## 🚀 Performance Check

- Dashboard loads in < 2 seconds
- Appointment list loads in < 1 second
- Actions complete in < 500ms
- No N+1 query issues (using select_related)
- Pagination works (10 per page)

## 📝 Test Data Requirements

To fully test, you need:
- At least 1 doctor account
- At least 1 mother account
- At least 5 appointments in different statuses:
  - 2 pending
  - 2 approved
  - 1 completed
- Appointments on different dates (today, tomorrow, past)

## 🎯 Success Criteria

**ALL features working** = Doctor can:
1. ✅ See all appointments immediately after mother books
2. ✅ Approve/decline pending appointments
3. ✅ Mark approved appointments as complete
4. ✅ Add medical notes (diagnosis, prescription, follow-up)
5. ✅ View complete patient history
6. ✅ Filter and search appointments
7. ✅ Receive and send notifications
8. ✅ Navigate without errors

**Test PASSED** ✅ when all 8 criteria are met!
