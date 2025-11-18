from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Baby, GrowthRecord, FeedingRecord, SleepRecord, DiaperRecord, VaccinationRecord, BabyMilestoneRecord
from .forms import BabyForm, GrowthRecordForm, FeedingRecordForm, SleepRecordForm, DiaperRecordForm, VaccinationRecordForm, BabyMilestoneRecordForm
from apps.accounts.models import UserProfile, Notification


@login_required
def baby_list(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Only mothers can access baby tracker
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can access the baby tracker.')
        return redirect('accounts:dashboard')
    
    babies = Baby.objects.filter(parent=request.user).order_by('-birth_date')
    
    return render(request, 'babytracker/list.html', {
        'babies': babies,
        'user_profile': user_profile,
    })


@login_required
def baby_create(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_profile.role != 'mother':
        messages.error(request, 'Only mothers can add babies.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = BabyForm(request.POST, request.FILES)
        if form.is_valid():
            baby = form.save(commit=False)
            baby.parent = request.user
            baby.save()
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                title='Baby Profile Created',
                message=f"Welcome {baby.name}! Baby profile has been created successfully.",
                notification_type='baby'
            )
            
            messages.success(request, f'{baby.name} has been added to your baby tracker!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = BabyForm()
    
    return render(request, 'babytracker/create.html', {'form': form})


@login_required
def baby_detail(request, pk):
    baby = get_object_or_404(Baby, pk=pk, parent=request.user)
    
    # Get recent records
    recent_growth = GrowthRecord.objects.filter(baby=baby)[:5]
    recent_feeding = FeedingRecord.objects.filter(baby=baby)[:5]
    recent_sleep = SleepRecord.objects.filter(baby=baby)[:5]
    recent_diaper = DiaperRecord.objects.filter(baby=baby)[:5]
    vaccination_records = VaccinationRecord.objects.filter(baby=baby)
    milestone_records = BabyMilestoneRecord.objects.filter(baby=baby)
    
    return render(request, 'babytracker/detail.html', {
        'baby': baby,
        'recent_growth': recent_growth,
        'recent_feeding': recent_feeding,
        'recent_sleep': recent_sleep,
        'recent_diaper': recent_diaper,
        'vaccination_records': vaccination_records,
        'milestone_records': milestone_records,
    })


@login_required
def baby_update(request, pk):
    baby = get_object_or_404(Baby, pk=pk, parent=request.user)
    
    if request.method == 'POST':
        form = BabyForm(request.POST, request.FILES, instance=baby)
        if form.is_valid():
            form.save()
            messages.success(request, f'{baby.name} has been updated successfully!')
            return redirect('babytracker:detail', pk=pk)
    else:
        form = BabyForm(instance=baby)
    
    return render(request, 'babytracker/update.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def baby_delete(request, pk):
    baby = get_object_or_404(Baby, pk=pk, parent=request.user)
    
    if request.method == 'POST':
        baby_name = baby.name
        baby.delete()
        messages.success(request, f'{baby_name} has been removed from your tracker.')
        return redirect('babytracker:list')
    
    return render(request, 'babytracker/delete.html', {'baby': baby})


@login_required
def growth_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = GrowthRecordForm(request.POST)
        if form.is_valid():
            growth_record = form.save(commit=False)
            growth_record.baby = baby
            growth_record.save()
            messages.success(request, 'Growth record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = GrowthRecordForm()
    
    return render(request, 'babytracker/growth_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def growth_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    growth_record = get_object_or_404(GrowthRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = GrowthRecordForm(request.POST, instance=growth_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Growth record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = GrowthRecordForm(instance=growth_record)
    
    return render(request, 'babytracker/growth_form.html', {
        'form': form,
        'baby': baby,
        'growth_record': growth_record,
    })


@login_required
def growth_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    growth_record = get_object_or_404(GrowthRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        growth_record.delete()
        messages.success(request, 'Growth record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/growth_delete.html', {
        'growth_record': growth_record,
        'baby': baby,
    })


@login_required
def feeding_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = FeedingRecordForm(request.POST)
        if form.is_valid():
            feeding_record = form.save(commit=False)
            feeding_record.baby = baby
            feeding_record.save()
            messages.success(request, 'Feeding record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = FeedingRecordForm()
    
    return render(request, 'babytracker/feeding_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def feeding_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    feeding_record = get_object_or_404(FeedingRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = FeedingRecordForm(request.POST, instance=feeding_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feeding record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = FeedingRecordForm(instance=feeding_record)
    
    return render(request, 'babytracker/feeding_form.html', {
        'form': form,
        'baby': baby,
        'feeding_record': feeding_record,
    })


@login_required
def feeding_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    feeding_record = get_object_or_404(FeedingRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        feeding_record.delete()
        messages.success(request, 'Feeding record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/feeding_delete.html', {
        'feeding_record': feeding_record,
        'baby': baby,
    })


@login_required
def sleep_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = SleepRecordForm(request.POST)
        if form.is_valid():
            sleep_record = form.save(commit=False)
            sleep_record.baby = baby
            sleep_record.save()
            messages.success(request, 'Sleep record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = SleepRecordForm()
    
    return render(request, 'babytracker/sleep_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def sleep_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    sleep_record = get_object_or_404(SleepRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = SleepRecordForm(request.POST, instance=sleep_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sleep record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = SleepRecordForm(instance=sleep_record)
    
    return render(request, 'babytracker/sleep_form.html', {
        'form': form,
        'baby': baby,
        'sleep_record': sleep_record,
    })


@login_required
def sleep_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    sleep_record = get_object_or_404(SleepRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        sleep_record.delete()
        messages.success(request, 'Sleep record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/sleep_delete.html', {
        'sleep_record': sleep_record,
        'baby': baby,
    })


@login_required
def diaper_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = DiaperRecordForm(request.POST)
        if form.is_valid():
            diaper_record = form.save(commit=False)
            diaper_record.baby = baby
            diaper_record.save()
            messages.success(request, 'Diaper record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = DiaperRecordForm()
    
    return render(request, 'babytracker/diaper_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def diaper_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    diaper_record = get_object_or_404(DiaperRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = DiaperRecordForm(request.POST, instance=diaper_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Diaper record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = DiaperRecordForm(instance=diaper_record)
    
    return render(request, 'babytracker/diaper_form.html', {
        'form': form,
        'baby': baby,
        'diaper_record': diaper_record,
    })


@login_required
def diaper_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    diaper_record = get_object_or_404(DiaperRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        diaper_record.delete()
        messages.success(request, 'Diaper record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/diaper_delete.html', {
        'diaper_record': diaper_record,
        'baby': baby,
    })


@login_required
def vaccination_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            vaccination_record = form.save(commit=False)
            vaccination_record.baby = baby
            vaccination_record.save()
            messages.success(request, 'Vaccination record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = VaccinationRecordForm()
    
    return render(request, 'babytracker/vaccination_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def vaccination_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    vaccination_record = get_object_or_404(VaccinationRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST, instance=vaccination_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vaccination record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = VaccinationRecordForm(instance=vaccination_record)
    
    return render(request, 'babytracker/vaccination_form.html', {
        'form': form,
        'baby': baby,
        'vaccination_record': vaccination_record,
    })


@login_required
def vaccination_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    vaccination_record = get_object_or_404(VaccinationRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        vaccination_record.delete()
        messages.success(request, 'Vaccination record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/vaccination_delete.html', {
        'vaccination_record': vaccination_record,
        'baby': baby,
    })


@login_required
def milestone_record_create(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    
    if request.method == 'POST':
        form = BabyMilestoneRecordForm(request.POST, request.FILES)
        if form.is_valid():
            milestone_record = form.save(commit=False)
            milestone_record.baby = baby
            milestone_record.save()
            messages.success(request, 'Milestone record added successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = BabyMilestoneRecordForm()
    
    return render(request, 'babytracker/milestone_form.html', {
        'form': form,
        'baby': baby,
    })


@login_required
def milestone_record_update(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    milestone_record = get_object_or_404(BabyMilestoneRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        form = BabyMilestoneRecordForm(request.POST, request.FILES, instance=milestone_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone record updated successfully!')
            return redirect('babytracker:detail', pk=baby.pk)
    else:
        form = BabyMilestoneRecordForm(instance=milestone_record)
    
    return render(request, 'babytracker/milestone_form.html', {
        'form': form,
        'baby': baby,
        'milestone_record': milestone_record,
    })


@login_required
def milestone_record_delete(request, baby_pk, pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    milestone_record = get_object_or_404(BabyMilestoneRecord, pk=pk, baby=baby)
    
    if request.method == 'POST':
        milestone_record.delete()
        messages.success(request, 'Milestone record deleted successfully!')
        return redirect('babytracker:detail', pk=baby.pk)
    
    return render(request, 'babytracker/milestone_delete.html', {
        'milestone_record': milestone_record,
        'baby': baby,
    })


@login_required
def growth_chart(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    growth_records = GrowthRecord.objects.filter(baby=baby).order_by('date')
    
    return render(request, 'babytracker/growth_chart.html', {
        'baby': baby,
        'growth_records': growth_records,
    })


@login_required
def feeding_chart(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    feeding_records = FeedingRecord.objects.filter(baby=baby).order_by('-date', '-time')[:30]
    
    return render(request, 'babytracker/feeding_chart.html', {
        'baby': baby,
        'feeding_records': feeding_records,
    })


@login_required
def sleep_chart(request, baby_pk):
    baby = get_object_or_404(Baby, pk=baby_pk, parent=request.user)
    sleep_records = SleepRecord.objects.filter(baby=baby).order_by('-date', '-start_time')[:30]
    
    return render(request, 'babytracker/sleep_chart.html', {
        'baby': baby,
        'sleep_records': sleep_records,
    })
