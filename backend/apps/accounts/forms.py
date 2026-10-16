from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
from .models import User, Profile
from .validators import normalize_avatar

class AdminUserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = (
            "email", "first_name", "last_name"
        )
    
    def clean_email(self):
        return User.objects.normalize_email(self.clean_data["email"])
    

class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
    

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if "avatar" in self.cleaned_data and avatar:
            return normalize_avatar(avatar)
        return avatar