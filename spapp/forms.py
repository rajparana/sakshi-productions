from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, User, Category

# categories = Category.objects.all().values_list('name','name') 
# category_list = []
# for category in categories:
#     category_list.append(category)

# users = User.objects.all().values_list('first_name','first_name')
# user_list = []
# for user in users:
#     user_list.append(user)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'destination', 'youtube', 'thumbnail', 'text')
    

class SignUpForm(UserCreationForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "mobile", "password1", "password2")


class LogInForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
