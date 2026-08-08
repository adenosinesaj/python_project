from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    C_profile, Product, Portfolio, 
    ChecklistTask, BudgetItem, EventSchedule
)


# ==========================================
# AUTHENTICATION & PROFILE FORMS
# ==========================================

class SignUpForm(forms.ModelForm):
    role = forms.ChoiceField(choices=C_profile.ROLE_CHOICES, required=True)
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Extra profile fields
    phone = forms.CharField(required=False, label="Phone")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Bio")
    address = forms.CharField(required=False, label="Address")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and picture.size > 5 * 1024 * 1024:  # 5 MB validation
            raise ValidationError("Profile picture file size must be under 5MB.")
        return picture

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile_pic = self.cleaned_data.get('profile_picture') or 'profile/user.png'

            C_profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                profile_picture=profile_pic,
                bio=self.cleaned_data.get('bio', ''),
                address=self.cleaned_data.get('address', ''),
                role=self.cleaned_data.get('role')
            )
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)  # <-- ADD required=False HERE

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = C_profile
        fields = ['phone', 'profile_picture', 'bio', 'address']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and hasattr(picture, 'size'):
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise ValidationError("Profile picture file size must be under 5MB.")
        return picture


# ==========================================
# VENDOR PRODUCT & PORTFOLIO FORMS
# ==========================================

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'p_photo', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'event_type', 'event_date', 'location', 'image', 'status', 'team_or_individual']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ==========================================
# EVENT PLANNING INTERACTIVE FORMS
# ==========================================

class ChecklistTaskForm(forms.ModelForm):
    class Meta:
        model = ChecklistTask
        fields = ['title', 'due_date', 'priority', 'is_completed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['title', 'category', 'estimated_cost', 'actual_cost']


class EventScheduleForm(forms.ModelForm):
    class Meta:
        model = EventSchedule
        fields = ['event_name', 'event_date', 'description']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }