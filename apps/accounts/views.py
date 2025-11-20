from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserProfileForm, DoctorProfileForm, AdminUserEditForm, AdminDoctorCreationForm
from .models import UserProfile, Notification


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.get_user()
        # Check if user account is deactivated
        try:
            if user.userprofile.account_status == 'deactivated':
                messages.error(self.request, 'Your account has been deactivated. Please contact support.')
                return self.form_invalid(form)
        except UserProfile.DoesNotExist:
            pass
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Baby Moms Care, {user.first_name}!')
            return redirect('accounts:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Redirect doctors to their specific dashboard
    if user_profile.role == 'doctor':
        return redirect('appointments:doctor_dashboard')
    
    # Redirect mothers to their specific dashboard  
    if user_profile.role == 'mother':
        return redirect('appointments:mother_dashboard')
    
    # Get recent notifications
    all_notifications = Notification.objects.filter(user=request.user)
    notifications = all_notifications[:5]
    unread_count = all_notifications.filter(is_read=False).count()
    
    # Check if user is new (first login)
    is_new_user = request.user.last_login is None
    
    # Dashboard statistics based on user role
    context = {
        'user_profile': user_profile,
        'notifications': notifications,
        'unread_count': unread_count,
        'is_new_user': is_new_user,
    }
    
    # Admin dashboard data
    if user_profile.role == 'admin':
        from django.contrib.auth.models import User
        from apps.appointments.models import Appointment
        
        total_users = User.objects.count()
        total_mothers = UserProfile.objects.filter(role='mother').count()
        total_doctors = UserProfile.objects.filter(role='doctor').count()
        
        all_appointments = Appointment.objects.all().order_by('-created_at')[:10]
        pending_appointments = Appointment.objects.filter(status='pending').count()
        today_appointments = Appointment.objects.filter(date=timezone.now().date()).count()
        
        context.update({
            'total_users': total_users,
            'total_mothers': total_mothers,
            'total_doctors': total_doctors,
            'recent_appointments': all_appointments,
            'pending_appointments': pending_appointments,
            'today_appointments': today_appointments,
        })
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        if user_profile.role == 'doctor':
            form = DoctorProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        if user_profile.role == 'doctor':
            form = DoctorProfileForm(instance=user_profile)
        else:
            form = UserProfileForm(instance=user_profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'user_profile': user_profile
    })


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user)
    
    # Mark all as read when viewing
    notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'accounts/notifications.html', {
        'notifications': notifications
    })


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('accounts:notifications')


@login_required
def logout_view(request):
    """Custom logout view with confirmation page"""
    if request.method == 'POST':
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'You have been successfully logged out. Thank you for using Baby Moms Care Clinic, {user_name}!')
        return redirect('accounts:login')
    
    return render(request, 'accounts/logout.html')


@login_required
def user_management_view(request):
    """Admin view to manage all users"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    users = User.objects.select_related('userprofile').all().order_by('-date_joined')
    
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(userprofile__role=role_filter)
    
    status_filter = request.GET.get('status')
    if status_filter:
        users = users.filter(userprofile__account_status=status_filter)
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'accounts/user_management.html', context)


@login_required
def toggle_user_status(request, user_id):
    """Toggle user account status between active and deactivated"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('accounts:user_management')
    
    try:
        profile = user.userprofile
        if profile.account_status == 'active':
            profile.account_status = 'deactivated'
            user.is_active = False
            messages.success(request, f'User {user.username} has been deactivated.')
        else:
            profile.account_status = 'active'
            user.is_active = True
            messages.success(request, f'User {user.username} has been reactivated.')
        
        profile.save()
        user.save()
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
    
    return redirect('accounts:user_management')


@login_required
def edit_user_view(request, user_id):
    """Admin view to edit user details"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user, profile_instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} has been updated successfully.')
            return redirect('accounts:user_management')
    else:
        form = AdminUserEditForm(instance=user, profile_instance=profile)
    
    return render(request, 'accounts/edit_user.html', {
        'form': form,
        'edited_user': user,
        'profile': profile
    })


@login_required
def delete_user_view(request, user_id):
    """Admin view to delete a user"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to perform this action.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('accounts:user_management')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted successfully.')
        return redirect('accounts:user_management')
    
    return render(request, 'accounts/delete_user.html', {'deleted_user': user})


@login_required
def create_doctor_view(request):
    """Admin-only view to create doctor accounts"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = AdminDoctorCreationForm(request.POST)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=User.objects.make_random_password()
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
            
            messages.success(request, f'Doctor account created successfully for {user.get_full_name()}.')
            return redirect('accounts:user_management')
    else:
        form = AdminDoctorCreationForm()
    
    return render(request, 'accounts/create_doctor.html', {'form': form})


@login_required
def create_admin_view(request):
    """Admin-only view to create admin accounts"""
    try:
        if request.user.userprofile.role != 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('accounts:dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone', '')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=User.objects.make_random_password()
            )
            
            # Create admin profile
            UserProfile.objects.create(
                user=user,
                role='admin',
                phone=phone
            )
            
            messages.success(request, f'Admin account created successfully for {user.get_full_name()}.')
            return redirect('accounts:user_management')
    
    return render(request, 'accounts/create_admin.html')
