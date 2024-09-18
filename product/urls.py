from django.urls import path
from .views import KitoblarView,KitobView,AddComment,Cart,AddKitobView,AddTilView,UpdatePlace,delete,cart_add,cart_summery,cart_update_plus,cart_update_remove,cart_delete,OrderView,History,users
# cart_delete,cart_update,cart_tasdiqlash
app_name='product'

urlpatterns = [
    path('',KitoblarView.as_view(),name='home'),
    path('addkitob/',AddKitobView.as_view(),name='addkitob'),
    path('addtil/',AddTilView.as_view(),name='addtil'),
    path('kitob/<int:id>',KitobView.as_view(),name='product_view'),
    path('update/<int:pk>',UpdatePlace.as_view(),name='update'),
    path('add_comment/<int:id>',AddComment.as_view(),name='add_comment'),
    path('cart/<int:id>',Cart,name='cart_kitob'),
    path('delete/<int:pk>/',delete,name='delete'),

    path('cart_add/',cart_add,name='cart_add'),
    path('cart_summery/',cart_summery,name='cart_summery'),

    # path('cart_update/',cart_update,name='cart_update'),
    path('cart_update_plus/',cart_update_plus,name='cart_plus'),
    path('cart_update_remove/',cart_update_remove,name='cart_remove'),

    path('cart_delete/',cart_delete,name='cart_delete'),
    path('order_view/',OrderView.as_view(),name='order_view'),
    path('orders/',History.as_view(),name='orders'),
    path('users/',users,name='user'),
]
