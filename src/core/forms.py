from django import forms

from core.models import UserProfile, Site


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email']


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'url']
