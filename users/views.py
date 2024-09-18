from django.shortcuts import render,redirect
from django.views.generic import ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import RegisterForm,LoginForm,UpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.info(request, "Registratsadan muffaqyatli o'ttingiz")
            return redirect('users:login')
    else:
        form = RegisterForm()
       
    return render(request, 'user/register.html', context={'form': form})

class LogInView(View):
    def get(self,request):
        form=LoginForm()
        return render(request,'user/login.html',context={'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'Sayitga maffaqyatli tashrif buyurdingiz')
                return redirect('product:home')

        return render(request,'user/login.html',context={'form':form})


class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.warning(request, 'Sayitdan chiqib ketingiz')
        return redirect('product:home')

class Profil(View):
    def get(self,request,pk):
        user_profil=User.objects.get(id=pk)
        return render(request,'user/profil.html',context={'user_profil':user_profil})
    
class UpdateView(LoginRequiredMixin,View):  
    def get(self,request,id):
        form=UpdateForm(instance=request.user)
        return render(request,'user/update.html',context={'form':form})
    def post(self,request,id):
        if request.method=='POST':
            form =UpdateForm(instance=request.user,data=request.POST,files=request.FILES)
            if form.is_valid():
                form.save()
                messages.warning(request,"Mufaqyatli O'zgartirildi")
                return redirect('product:home')

        return render(request, 'user/update.html', context={'form': form})
    







# serializers
    

        