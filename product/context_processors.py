from .models import Catigory
from .cart import Cart_Product
from users.models import User

def users(request):
    return {"users":User.objects.all()}

def catigory(request):
    return {"catigory":Catigory.objects.all()}

def cart(request):
    return {"cart":Cart_Product(request)}
