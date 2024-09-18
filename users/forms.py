from .models import User
from django import forms

# Yo'yhatdan o'tish
class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(required=True, label='First_name', widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(required=True, label='Last_name', widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required=True, label='Email',widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password_config = forms.CharField(required=True, label='Password_config', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    img = forms.ImageField(required=True, label='Image', widget=forms.FileInput(attrs={'class': "form-control"}))
    photo=forms.CharField(required=True,label='Phone_number',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password','password_config','img','photo']

    def clean_password_config(self):
        password=self.cleaned_data['password']
        password_config = self.cleaned_data['password_config']

        if password != password_config:
            raise forms.ValidationError("Parrolaringizni qayta solishtiring")
        return password

    def clean_username(self):
        username=self.cleaned_data["username"]

        if len('username')<5 or len('username')>30:
            raise forms.ValidationError("Usernamegiz 5-30 oraligida bo'lish kerak")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bunday email mavjud")

        elif not (email.endswith('@gmail.com') or email.endswith('@mail.ru')):
            raise forms.ValidationError("Enter a valid email address.")

        return email



# Login qilish
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(required=True, label='Password',widget=forms.PasswordInput(attrs={'class': "form-control"}))

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 5 or len(username) > 30:
            raise forms.ValidationError("Usernamegiz 5-30 oraligida bo'lish kerak")

        return username
    
class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','img','user_phone']