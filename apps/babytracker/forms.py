from django import forms
from django.utils import timezone
from .models import Baby, GrowthRecord, FeedingRecord, SleepRecord, DiaperRecord, VaccinationRecord, BabyMilestoneRecord, Vaccination, Milestone


class BabyForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ['name', 'gender', 'birth_date', 'birth_weight', 'birth_height', 'photo', 'notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
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
            elif field_name == 'photo':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })


class GrowthRecordForm(forms.ModelForm):
    class Meta:
        model = GrowthRecord
        fields = ['date', 'weight', 'height', 'head_circumference', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date to today
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        
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


class FeedingRecordForm(forms.ModelForm):
    class Meta:
        model = FeedingRecord
        fields = ['date', 'time', 'feeding_type', 'duration_minutes', 'amount_ml', 'food_description', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'food_description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date and time
        if not self.instance.pk:
            now = timezone.now()
            self.fields['date'].initial = now.date()
            self.fields['time'].initial = now.time()
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name in ['food_description', 'notes']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })


class SleepRecordForm(forms.ModelForm):
    class Meta:
        model = SleepRecord
        fields = ['date', 'start_time', 'end_time', 'sleep_quality', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
        
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


class DiaperRecordForm(forms.ModelForm):
    class Meta:
        model = DiaperRecord
        fields = ['date', 'time', 'diaper_type', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date and time
        if not self.instance.pk:
            now = timezone.now()
            self.fields['date'].initial = now.date()
            self.fields['time'].initial = now.time()
        
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


class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['vaccination', 'date_given', 'doctor_name', 'clinic_name', 'batch_number', 'next_due_date', 'side_effects', 'notes']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'side_effects': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date
        if not self.instance.pk:
            self.fields['date_given'].initial = timezone.now().date()
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name in ['side_effects', 'notes']:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })


class BabyMilestoneRecordForm(forms.ModelForm):
    class Meta:
        model = BabyMilestoneRecord
        fields = ['milestone', 'date_achieved', 'notes', 'photo']
        widgets = {
            'date_achieved': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date()}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default date
        if not self.instance.pk:
            self.fields['date_achieved'].initial = timezone.now().date()
        
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'notes':
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
