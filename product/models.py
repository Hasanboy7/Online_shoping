from django.db import models
from users.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from users.models import User
from django.utils import timezone
# from .cart import Cart_Product


# Create your models here.

class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Catigory(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    cart_img=models.ImageField(upload_to='tillar/',null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user')
    category = models.ForeignKey(Catigory, related_name='products', on_delete=models.CASCADE)
    price=models.CharField(max_length=200)
    soni=models.IntegerField(default=0)
    body=models.TextField(null=True,blank=True)
    img=models.ImageField(upload_to='product/',null=True,blank=True)
    create_date=models.DateTimeField(auto_now=True)
    update_date=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    place=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='izohlar',null=True,blank=True)
    comment_text=models.TextField()
    start_give=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    create_at=models.DateField(default=timezone.now)
    # time_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.start_give)

class Order(BaseModel):
    order_id=models.CharField(max_length=50)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    def __str__(self):
        return self.order_id

class OrderItem(BaseModel):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='item')
    product_id=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    price=models.CharField(max_length=200)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} -- Quantity {self.quantity}"

    @property
    def total_price(self):
        return self.price*self.quantity



