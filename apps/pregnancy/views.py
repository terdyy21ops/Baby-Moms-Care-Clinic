from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from .models import PregnancyLog, PregnancyWeeklyLog, PregnancyMilestone, PregnancyReminder, PregnancyTip
from .forms import PregnancyLogForm, PregnancyWeeklyLogForm, PregnancyMilestoneForm, PregnancyReminderForm
from apps.accounts.models import UserProfile, Notification
from apps.appointments.models import Appointment


@login_required
def pregnancy_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Only mothers can access pregnancy tracker
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can access the pregnancy tracker.')
        return redirect('accounts:dashboard')
    
    # Get active pregnancy
    active_pregnancy = PregnancyLog.objects.filter(user=request.user, is_active=True).first()
    
    # Get recent appointments
    recent_appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by('-date', '-time')[:3]
    
    context = {
        'active_pregnancy': active_pregnancy,
        'user_profile': user_profile,
        'recent_appointments': recent_appointments,
    }
    
    if active_pregnancy:
        # Get recent weekly logs
        recent_logs = PregnancyWeeklyLog.objects.filter(pregnancy=active_pregnancy)[:3]
        
        # Get upcoming reminders
        upcoming_reminders = PregnancyReminder.objects.filter(
            pregnancy=active_pregnancy,
            is_active=True,
            start_date__gte=timezone.now().date()
        )[:5]
        
        # Get relevant tips for current trimester
        tips = PregnancyTip.objects.filter(
            Q(trimester=active_pregnancy.trimester) | Q(trimester=0),
            is_active=True
        )[:3]
        
        # Get recent milestones
        recent_milestones = PregnancyMilestone.objects.filter(pregnancy=active_pregnancy)[:3]
        
        context.update({
            'recent_logs': recent_logs,
            'upcoming_reminders': upcoming_reminders,
            'tips': tips,
            'recent_milestones': recent_milestones,
        })
    
    return render(request, 'pregnancy/dashboard.html', context)


@login_required
def pregnancy_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can access pregnancy records.')
        return redirect('accounts:dashboard')
    
    pregnancies = PregnancyLog.objects.filter(user=request.user)
    
    return render(request, 'pregnancy/list.html', {
        'pregnancies': pregnancies,
        'user_profile': user_profile,
    })


@login_required
def pregnancy_create(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can create pregnancy records.')
        return redirect('accounts:dashboard')
    
    # Check if user already has an active pregnancy
    active_pregnancy = PregnancyLog.objects.filter(user=request.user, is_active=True).exists()
    if active_pregnancy:
        messages.warning(request, 'You already have an active pregnancy. Please complete it before starting a new one.')
        return redirect('pregnancy:dashboard')
    
    if request.method == 'POST':
        form = PregnancyLogForm(request.POST)
        if form.is_valid():
            pregnancy = form.save(commit=False)
            pregnancy.user = request.user
            pregnancy.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                title='Pregnancy Tracker Started',
                message=f'Your pregnancy journey has been started! Due date: {pregnancy.due_date}',
                notification_type='pregnancy'
            )
            
            messages.success(request, 'Pregnancy tracker created successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyLogForm()
    
    return render(request, 'pregnancy/create.html', {'form': form})


@login_required
def pregnancy_detail(request, pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pk, user=request.user)
    
    # Get weekly logs
    weekly_logs = PregnancyWeeklyLog.objects.filter(pregnancy=pregnancy)
    
    # Get milestones
    milestones = PregnancyMilestone.objects.filter(pregnancy=pregnancy)
    
    # Get reminders
    reminders = PregnancyReminder.objects.filter(pregnancy=pregnancy, is_active=True)
    
    # Get relevant tips
    tips = PregnancyTip.objects.filter(
        Q(trimester=pregnancy.trimester) | Q(trimester=0),
        is_active=True
    )
    
    return render(request, 'pregnancy/detail.html', {
        'pregnancy': pregnancy,
        'weekly_logs': weekly_logs,
        'milestones': milestones,
        'reminders': reminders,
        'tips': tips,
    })


@login_required
def pregnancy_update(request, pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PregnancyLogForm(request.POST, instance=pregnancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pregnancy record updated successfully!')
            return redirect('pregnancy:detail', pk=pk)
    else:
        form = PregnancyLogForm(instance=pregnancy)
    
    return render(request, 'pregnancy/update.html', {
        'form': form,
        'pregnancy': pregnancy,
    })


@login_required
def weekly_log_create(request, pregnancy_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    
    if request.method == 'POST':
        form = PregnancyWeeklyLogForm(request.POST, request.FILES, pregnancy=pregnancy)
        if form.is_valid():
            weekly_log = form.save(commit=False)
            weekly_log.pregnancy = pregnancy
            weekly_log.save()
            messages.success(request, 'Weekly log added successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyWeeklyLogForm(pregnancy=pregnancy)
    
    return render(request, 'pregnancy/weekly_log_form.html', {
        'form': form,
        'pregnancy': pregnancy,
    })


@login_required
def weekly_log_update(request, pregnancy_pk, log_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    weekly_log = get_object_or_404(PregnancyWeeklyLog, pk=log_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        form = PregnancyWeeklyLogForm(request.POST, request.FILES, instance=weekly_log, pregnancy=pregnancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Weekly log updated successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyWeeklyLogForm(instance=weekly_log, pregnancy=pregnancy)
    
    return render(request, 'pregnancy/weekly_log_form.html', {
        'form': form,
        'pregnancy': pregnancy,
        'weekly_log': weekly_log,
    })


@login_required
def weekly_log_delete(request, pregnancy_pk, log_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    weekly_log = get_object_or_404(PregnancyWeeklyLog, pk=log_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        weekly_log.delete()
        messages.success(request, 'Weekly log deleted successfully!')
        return redirect('pregnancy:detail', pk=pregnancy.pk)
    
    return render(request, 'pregnancy/weekly_log_delete.html', {
        'weekly_log': weekly_log,
        'pregnancy': pregnancy,
    })


@login_required
def milestone_create(request, pregnancy_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    
    if request.method == 'POST':
        form = PregnancyMilestoneForm(request.POST, pregnancy=pregnancy)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.pregnancy = pregnancy
            milestone.save()
            messages.success(request, 'Milestone added successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyMilestoneForm(pregnancy=pregnancy)
    
    return render(request, 'pregnancy/milestone_form.html', {
        'form': form,
        'pregnancy': pregnancy,
    })


@login_required
def milestone_update(request, pregnancy_pk, milestone_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    milestone = get_object_or_404(PregnancyMilestone, pk=milestone_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        form = PregnancyMilestoneForm(request.POST, instance=milestone, pregnancy=pregnancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone updated successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyMilestoneForm(instance=milestone, pregnancy=pregnancy)
    
    return render(request, 'pregnancy/milestone_form.html', {
        'form': form,
        'pregnancy': pregnancy,
        'milestone': milestone,
    })


@login_required
def milestone_delete(request, pregnancy_pk, milestone_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    milestone = get_object_or_404(PregnancyMilestone, pk=milestone_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        milestone.delete()
        messages.success(request, 'Milestone deleted successfully!')
        return redirect('pregnancy:detail', pk=pregnancy.pk)
    
    return render(request, 'pregnancy/milestone_delete.html', {
        'milestone': milestone,
        'pregnancy': pregnancy,
    })


@login_required
def reminder_create(request, pregnancy_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    
    if request.method == 'POST':
        form = PregnancyReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.pregnancy = pregnancy
            reminder.save()
            messages.success(request, 'Reminder created successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyReminderForm()
    
    return render(request, 'pregnancy/reminder_form.html', {
        'form': form,
        'pregnancy': pregnancy,
    })


@login_required
def reminder_update(request, pregnancy_pk, reminder_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    reminder = get_object_or_404(PregnancyReminder, pk=reminder_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        form = PregnancyReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder updated successfully!')
            return redirect('pregnancy:detail', pk=pregnancy.pk)
    else:
        form = PregnancyReminderForm(instance=reminder)
    
    return render(request, 'pregnancy/reminder_form.html', {
        'form': form,
        'pregnancy': pregnancy,
        'reminder': reminder,
    })


@login_required
def reminder_delete(request, pregnancy_pk, reminder_pk):
    pregnancy = get_object_or_404(PregnancyLog, pk=pregnancy_pk, user=request.user)
    reminder = get_object_or_404(PregnancyReminder, pk=reminder_pk, pregnancy=pregnancy)
    
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Reminder deleted successfully!')
        return redirect('pregnancy:detail', pk=pregnancy.pk)
    
    return render(request, 'pregnancy/reminder_delete.html', {
        'reminder': reminder,
        'pregnancy': pregnancy,
    })
