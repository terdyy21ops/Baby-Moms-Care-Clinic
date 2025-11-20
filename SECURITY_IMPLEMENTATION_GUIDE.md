# 🔒 Security Implementation Guide - Baby Moms Care Clinic

## ✅ Changes Implemented

### 1. Secured Public Registration
- ✅ Removed role selection from registration form
- ✅ All public registrations automatically set to 'mother' role
- ✅ Backend validation prevents role manipulation

### 2. Files Modified
- ✅ `apps/accounts/forms.py` - Removed role field, hardcoded to 'mother'
- ✅ `templates/accounts/register.html` - Removed role selection UI
- ✅ `apps/accounts/models.py` - Added DoctorApplication model
- ✅ `apps/accounts/decorators.py` - Created role-based access control

## 📋 Additional Steps Required

### Step 1: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Admin Doctor Creation View

Add to `apps/accounts/views.py`:

```python
from .decorators import admin_required
from .forms import AdminDoctorCreationForm
from django.contrib.auth.hashers import make_random_password
from django.core.mail import send_mail

@admin_required
def create_doctor_view(request):
    if request.method == 'POST':
        form = AdminDoctorCreationForm(request.POST)
        if form.is_valid():
            # Generate temporary password
            temp_password = make_random_password(length=12)
            
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=temp_password,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Create doctor profile
            UserProfile.objects.create(
                user=user,
                role='doctor',
                phone=form.cleaned_data['phone'],
                license_number=form.cleaned_data['license_number'],
                specialization=form.cleaned_data['specialization'],
                years_experience=form.cleaned_data.get('years_experience', 0)
            )
            
            # Send email with credentials
            send_mail(
                'Your Doctor Account - Baby Moms Care Clinic',
                f'Your account has been created.\\nUsername: {user.username}\\nTemporary Password: {temp_password}\\nPlease change your password after first login.',
                'noreply@babymomscare.com',
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Doctor account created for {user.get_full_name()}. Credentials sent to {user.email}')
            return redirect('accounts:user_management')
    else:
        form = AdminDoctorCreationForm()
    
    return render(request, 'accounts/create_doctor.html', {'form': form})
```

### Step 3: Add URL Patterns

Add to `apps/accounts/urls.py`:

```python
path('admin/create-doctor/', views.create_doctor_view, name='create_doctor'),
path('admin/doctor-applications/', views.doctor_applications_view, name='doctor_applications'),
path('admin/approve-application/<int:app_id>/', views.approve_application, name='approve_application'),
path('admin/reject-application/<int:app_id>/', views.reject_application, name='reject_application'),
path('apply-doctor/', views.doctor_application_view, name='doctor_application'),
```

### Step 4: Protect Existing Views

Update views in `apps/accounts/views.py`:

```python
from .decorators import admin_required, role_required

# Add decorator to user_management_view
@admin_required
def user_management_view(request):
    # existing code...

# Add decorator to toggle_user_status
@admin_required
def toggle_user_status(request, user_id):
    # existing code...

# Add decorator to edit_user_view
@admin_required
def edit_user_view(request, user_id):
    # existing code...

# Add decorator to delete_user_view
@admin_required
def delete_user_view(request, user_id):
    # existing code...
```

### Step 5: Create Doctor Application View

```python
def doctor_application_view(request):
    \"\"\"Public form for doctors to apply\"\"\"
    if request.method == 'POST':
        # Handle form submission
        # Create DoctorApplication instance
        # Send confirmation email
        messages.success(request, 'Your application has been submitted. You will be notified once reviewed.')
        return redirect('home')
    
    return render(request, 'accounts/doctor_application.html')
```

### Step 6: Create Templates

#### `templates/accounts/create_doctor.html`
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Create Doctor Account{% endblock %}

{% block content %}
<div class=\"max-w-2xl mx-auto py-8\">
    <div class=\"bg-white rounded-2xl shadow-xl p-8\">
        <h1 class=\"text-3xl font-bold text-rose-600 mb-6\">Create Doctor Account</h1>
        
        <form method=\"post\" class=\"space-y-4\">
            {% csrf_token %}
            {{ form.as_p }}
            
            <button type=\"submit\" class=\"w-full bg-gradient-to-r from-pink-500 to-rose-500 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-all\">
                Create Doctor Account
            </button>
        </form>
    </div>
</div>
{% endblock %}
```

### Step 7: Update Admin Dashboard

Add button to create doctor in user management page:

```html
<a href=\"{% url 'accounts:create_doctor' %}\" class=\"bg-gradient-to-r from-pink-500 to-rose-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all\">
    <i data-lucide=\"user-plus\"></i>
    Create Doctor Account
</a>
```

### Step 8: Prevent Role Manipulation in Admin Edit

Update `AdminUserEditForm` to prevent changing admin roles:

```python
def clean_role(self):
    role = self.cleaned_data.get('role')
    if self.profile_instance and self.profile_instance.role == 'admin':
        # Prevent changing admin role
        if role != 'admin':
            raise forms.ValidationError('Cannot change admin role')
    return role
```

## 🔐 Security Features Implemented

### ✅ Completed
1. Public registration only creates 'mother' accounts
2. Role field removed from frontend
3. Backend validation prevents role manipulation
4. Role-based access control decorators created
5. Doctor application model created

### 🚧 To Complete
1. Run migrations for DoctorApplication model
2. Create admin doctor creation view and template
3. Add doctor application form and workflow
4. Protect all existing views with decorators
5. Add email notifications for doctor accounts
6. Create doctor application review interface

## 🎨 Rose Pink Theme

All new forms and pages use the rose-pink theme:
- Primary: `#e11d8f`
- Secondary: `#f472b6`
- Gradient: `from-pink-500 to-rose-500`

## 🧪 Testing Checklist

- [ ] Try to register as doctor/admin (should fail)
- [ ] Try to modify role via browser inspector (should fail)
- [ ] Admin can create doctor accounts
- [ ] Doctor receives email with credentials
- [ ] Doctor can login and change password
- [ ] Non-admin cannot access admin pages
- [ ] Doctor cannot access admin pages
- [ ] Mother cannot access doctor pages

## 📧 Email Configuration

Configure in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Baby Moms Care <noreply@babymomscare.com>'
```

## 🚀 Deployment Notes

1. Set `DEBUG = False` in production
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Set proper `ALLOWED_HOSTS`
5. Use strong `SECRET_KEY`

---

**Status**: ✅ Core Security Implemented
**Next Steps**: Complete remaining views and templates
**Priority**: HIGH - Security Critical
