# forms.py

from django import forms
from .models import Story
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar', 'phone_number', 'website', 
                  'occupation', 'twitter', 'linkedin', 'github', 'receive_newsletter', 
                  'dark_mode', 'gender', 'interests')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'neumorphic-input w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'content': forms.Textarea(attrs={'class': 'neumorphic-input w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'rows': 10}),
        }

    