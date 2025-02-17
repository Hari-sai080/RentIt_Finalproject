from django import forms
from .models import Property
from django.contrib.auth.models import User
from .models import Property, PropertyImage, Review, Profile, Message, BlogPost

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'role']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'role']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']