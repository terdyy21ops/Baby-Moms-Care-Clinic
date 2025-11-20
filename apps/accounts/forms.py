from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)
    # Role is removed from public registration - always set to 'mother'
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
            })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create user profile - ALWAYS set role to 'mother' for public registration
            UserProfile.objects.create(
                user=user,
                role='mother',  # Hardcoded - cannot be changed from frontend
                phone=self.cleaned_data.get('phone', '')
            )
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'date_of_birth', 'address', 'profile_picture', 
                 'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind CSS classes
        for field_name, field in self.fields.items():
            if field_name == 'address':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent resize-none'
                })
            elif field_name == 'profile_picture':
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-300 focus:border-transparent'
                })
        
        # Set initial values for user fields
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update user fields
        if profile.user:
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            if commit:
                profile.user.save()
        
        if commit:
            profile.save()
        return profile


class DoctorProfileForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        fields = UserProfileForm.Meta.fields + ['license_number', 'specialization', 'years_experience']


class AdminDoctorCreationForm(forms.Form):
    """Form for admin to create doctor accounts"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=15, required=True)
    license_number = forms.CharField(max_length=50, required=True, label='PRC/License Number')
    specialization = forms.CharField(max_length=100, required=True)
    years_experience = forms.IntegerField(required=False, min_value=0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-pink-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent'
            })
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email


class AdminUserEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES, required=True)
    phone = forms.CharField(max_length=15, required=False)
    
    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('instance', None)
        self.profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)
        
        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
        
        if self.profile_instance:
            self.fields['role'].initial = self.profile_instance.role
            self.fields['phone'].initial = self.profile_instance.phone
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent'
            })
    
    def save(self):
        if self.user_instance:
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name = self.cleaned_data['last_name']
            self.user_instance.email = self.cleaned_data['email']
            self.user_instance.save()
        
        if self.profile_instance:
            self.profile_instance.role = self.cleaned_data['role']
            self.profile_instance.phone = self.cleaned_data['phone']
            self.profile_instance.save()
        
        return self.user_instance
