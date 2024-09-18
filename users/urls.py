from django.urls import path
from .views import LogInView,register,LogOutView,UpdateView,Profil

app_name='users'
urlpatterns = [
    path('login/',LogInView.as_view(),name='login'),
    path('register/',register,name='register'),
    path('logout/',LogOutView.as_view(),name='logout'),
    path('update/<int:id>/', UpdateView.as_view(), name="update"),
    path('profil/<int:pk>/', Profil.as_view(), name="profil"),
]