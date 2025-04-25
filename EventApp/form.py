from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import C_profile
from django.core.exceptions import ValidationError

# SignUpForm (no change)
class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Extra fields for profile
    phone = forms.CharField(required=False, label="Phone")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile_pic = self.cleaned_data.get('profile_picture')
            if not profile_pic:
                profile_pic = 'profile/user.png'  # Default image path

            C_profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                profile_picture=profile_pic,
                bio=self.cleaned_data.get('bio')
            )
        return user

# ProfilePictureForm to handle profile picture updates
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = C_profile
        fields = ['profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("Profile picture is too large. Maximum size is 5MB.")
        return profile_picture
