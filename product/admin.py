from django.contrib import admin
from .models import Comment,Catigory,Product,Order,OrderItem
# Register your models here.

class Products(admin.ModelAdmin):
    list_display=('id','name','category','price','soni','create_date','update_date')
    list_display_links=['name']
    search_fields=['name',]

class Orders(admin.ModelAdmin):
    list_display=('order_id','total_price','user','create_date','update_date')
    list_display_links=['user']
    search_fields=['order_id',]

admin.site.register(Product,Products)
admin.site.register(Catigory)
admin.site.register(Comment)
admin.site.register(Order,Orders)
admin.site.register(OrderItem)