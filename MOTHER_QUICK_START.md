# Mother Dashboard - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Run the Server
```bash
python manage.py runserver
```

### Step 2: Log in as Mother
```
URL: http://127.0.0.1:8000/accounts/login/
Username: [your mother account]
Password: [your password]
```

### Step 3: Access Mother Dashboard
```
URL: http://127.0.0.1:8000/appointments/mother-dashboard/
```

---

## 🎯 Quick Actions

### Book an Appointment
1. Click "Book Appointment" card on dashboard
2. Select doctor from dropdown
3. Choose date and time
4. Click "Book Appointment"
5. Done! Status: Pending

### View Doctors
1. Click "View Doctors" card on dashboard
2. Browse doctor profiles
3. Click "Book Appointment" on any doctor
4. Fill form and submit

### Manage Appointments
1. Click "All Appointments" card
2. Filter by status if needed
3. Click "View Details" on any appointment
4. Use "Reschedule" or "Cancel" buttons

---

## 📍 Important URLs

| Page | URL |
|------|-----|
| Mother Dashboard | `/appointments/mother-dashboard/` |
| Doctor Directory | `/appointments/doctors/` |
| Book Appointment | `/appointments/create/` |
| All Appointments | `/appointments/` |
| My Profile | `/accounts/profile/` |
| Notifications | `/accounts/notifications/` |

---

## 🎨 Status Colors

- 🟡 **Pending** = Waiting for approval
- 🟢 **Approved** = Confirmed by doctor
- 🔵 **Completed** = Visit finished
- 🔴 **Cancelled** = Appointment cancelled

---

## ⚠️ Important Rules

### Booking
- ✅ Can book future dates only
- ✅ System checks doctor availability
- ✅ Prevents double-booking

### Cancelling
- ✅ Can cancel before appointment day
- ❌ Cannot cancel on appointment day
- ❌ Cannot cancel if completed

### Rescheduling
- ✅ Can reschedule if not past
- ✅ Can reschedule if pending/approved
- ❌ Cannot reschedule if completed/cancelled

---

## 🔔 Notifications

You'll receive notifications when:
- ✅ Doctor approves your appointment
- ✅ Appointment status changes
- ✅ Appointment is completed
- ✅ Appointment is cancelled

**Check**: Click bell icon in navbar

---

## 🆘 Need Help?

### Cannot book appointment?
- Check date is in future
- Try different time slot
- Verify doctor availability

### Cannot cancel?
- Check appointment is not today
- Verify status is pending/approved

### Doctor not showing?
- Check search filters
- Verify doctor is active

---

## ✅ Quick Test

1. ✅ Access mother dashboard
2. ✅ View doctor directory
3. ✅ Book test appointment
4. ✅ View appointment details
5. ✅ Cancel appointment (if future)

---

## 📱 Mobile Access

All features work on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers

---

## 🎉 You're Ready!

Start managing your healthcare appointments with ease!

**Dashboard**: `/appointments/mother-dashboard/`

---

**Questions?** Check `MOTHER_DASHBOARD_GUIDE.md` for detailed documentation.
