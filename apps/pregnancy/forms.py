from django import forms
from django.utils import timezone
from .models import PregnancyLog, PregnancyWeeklyLog, PregnancyMilestone, PregnancyReminder


class PregnancyLogForm(forms.ModelForm):
    class Meta:
        model = PregnancyLog
        fields = ['start_date', 'due_date', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'notes':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        
        if start_date and due_date:
            # Check if due date is after start date
            if due_date <= start_date:
                raise forms.ValidationError("Due date must be after the start date.")
            
            # Check if the pregnancy duration is reasonable (between 20-45 weeks)
            duration = (due_date - start_date).days
            if duration < 140:  # 20 weeks
                raise forms.ValidationError("Pregnancy duration seems too short. Please check your dates.")
            elif duration > 315:  # 45 weeks
                raise forms.ValidationError("Pregnancy duration seems too long. Please check your dates.")
        
        return cleaned_data


class PregnancyWeeklyLogForm(forms.ModelForm):
    class Meta:
        model = PregnancyWeeklyLog
        fields = ['week_number', 'weight', 'symptoms', 'mood', 'energy_level', 'notes', 'photo']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'energy_level': forms.Select(choices=[(i, f"{i}/10") for i in range(1, 11)]),
        }
    
    def __init__(self, *args, **kwargs):
        self.pregnancy = kwargs.pop('pregnancy', None)
        super().__init__(*args, **kwargs)
        
        # Set week number based on current pregnancy week
        if self.pregnancy and not self.instance.pk:
            current_week = self.pregnancy.current_week
            if current_week:
                self.fields['week_number'].initial = current_week
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name in ['symptoms', 'notes']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            elif field_name == 'photo':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
    
    def clean_week_number(self):
        week_number = self.cleaned_data.get('week_number')
        
        if week_number and (week_number < 1 or week_number > 42):
            raise forms.ValidationError("Week number must be between 1 and 42.")
        
        return week_number


class PregnancyMilestoneForm(forms.ModelForm):
    class Meta:
        model = PregnancyMilestone
        fields = ['title', 'description', 'milestone_type', 'date', 'week_number', 'is_important']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        self.pregnancy = kwargs.pop('pregnancy', None)
        super().__init__(*args, **kwargs)
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            elif field_name == 'is_important':
                field.widget.attrs.update({
                    'class': 'rounded border-pink-200 text-pink-600 focus:ring-pink-300'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })


class PregnancyReminderForm(forms.ModelForm):
    class Meta:
        model = PregnancyReminder
        fields = ['title', 'description', 'reminder_type', 'frequency', 'start_date', 'end_date', 'time', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            elif field_name == 'is_active':
                field.widget.attrs.update({
                    'class': 'rounded border-pink-200 text-pink-600 focus:ring-pink-300'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        frequency = cleaned_data.get('frequency')
        
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date.")
        
        if frequency != 'once' and not end_date:
            raise forms.ValidationError("End date is required for recurring reminders.")
        
        return cleaned_data
