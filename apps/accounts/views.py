from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm, UserProfileForm, DoctorProfileForm
from .models import UserProfile, Notification


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
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
    
    # Get recent notifications
    all_notifications = Notification.objects.filter(user=request.user)
    notifications = all_notifications[:5]
    unread_count = all_notifications.filter(is_read=False).count()
    
    # Dashboard statistics based on user role
    context = {
        'user_profile': user_profile,
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    if user_profile.role == 'mother':
        # Get mother-specific data
        from apps.appointments.models import Appointment
        from apps.pregnancy.models import PregnancyLog
        from apps.babytracker.models import Baby
        
        upcoming_appointments = Appointment.objects.filter(
            patient=request.user,
            date__gte=timezone.now().date()
        ).order_by('date', 'time')[:3]
        
        pregnancy_logs = PregnancyLog.objects.filter(user=request.user).order_by('-created_at')[:1]
        babies = Baby.objects.filter(parent=request.user).order_by('-birth_date')[:3]
        
        context.update({
            'upcoming_appointments': upcoming_appointments,
            'pregnancy_logs': pregnancy_logs,
            'babies': babies,
        })
    
    elif user_profile.role == 'doctor':
        # Get doctor-specific data
        from apps.appointments.models import Appointment
        
        today_appointments = Appointment.objects.filter(
            doctor=request.user,
            date=timezone.now().date()
        ).order_by('time')
        
        upcoming_appointments = Appointment.objects.filter(
            doctor=request.user,
            date__gt=timezone.now().date()
        ).order_by('date', 'time')[:5]
        
        context.update({
            'today_appointments': today_appointments,
            'upcoming_appointments': upcoming_appointments,
        })
    
    elif user_profile.role == 'admin':
        # Get admin-specific data
        from django.contrib.auth.models import User
        from apps.appointments.models import Appointment
        from apps.articles.models import Article
        from apps.forum.models import Post
        
        total_users = User.objects.count()
        total_mothers = UserProfile.objects.filter(role='mother').count()
        total_doctors = UserProfile.objects.filter(role='doctor').count()
        
        recent_appointments = Appointment.objects.order_by('-created_at')[:5]
        recent_articles = Article.objects.order_by('-created_at')[:3]
        recent_posts = Post.objects.order_by('-created_at')[:3]
        
        context.update({
            'total_users': total_users,
            'total_mothers': total_mothers,
            'total_doctors': total_doctors,
            'recent_appointments': recent_appointments,
            'recent_articles': recent_articles,
            'recent_posts': recent_posts,
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
