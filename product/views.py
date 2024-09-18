from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import ListView,DetailView
from .models import Product,Catigory,Comment,Order,OrderItem
from .forms import CommentForm,AddKitob,AddTilForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse,JsonResponse
from .cart import Cart_Product
from django.core.exceptions import ValidationError
import uuid
from users.models import User

# Create your views here.

class KitoblarView(View):

    def get(self,request):
        cart = Cart_Product(request)
        all_products=cart.get_all_info()
        products = Catigory.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
        categories_with_products = {category: Product.objects.filter(category=category) for category in products}
        product=Product.objects.all()
        search_query=request.GET.get('q',"")
        
        if search_query:
            products = product.filter(name__icontains=search_query)
            print(products)
            # Mahsulotlar uchun to'g'ri kategoriyalarni olamiz
            categories_with_products = {
            category: Product.objects.filter(category=category, name__icontains=search_query)
            for category in Catigory.objects.filter(id__in=products.values('category_id'))
        }
        # print(categories_with_products)

        date={
            'products':products,
            'all_products': all_products,
            'categories_with_products':categories_with_products,
            'search_query':search_query
        }
        return render(request,'home.html',context=date)

def users(request):
    user=User.objects.all()

    return render(request,'product/users.html',{'users':user})



class KitobView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        form = CommentForm()
        return render(request, 'product/detail.html', {'product': product, 'form': form})


class AddComment(LoginRequiredMixin, View):
    def post(self, request, id):
        place = Product.objects.get(id=id)  # Mahsulot mavjudligini tekshiradi yoki 404 qaytaradi
        form = CommentForm(request.POST)
        start_give = Comment.objects.all()
        
        # Ushbu foydalanuvchi tomonidan ushbu mahsulotga izoh qoldirilganligini tekshiramiz
        existing_comment = Comment.objects.filter(user=request.user, place=place).first()
        
        if existing_comment:
            # Agar izoh allaqachon mavjud bo'lsa, xabar qaytarish yoki izohni yangilash mumkin
            messages.error(request, "Siz allaqachon ushbu mahsulotga izoh qoldirgansiz.")
            return redirect(reverse('product:product_view', kwargs={'id': place.id}))
        
        
        if form.is_valid():
                
            Comment.objects.create(
                user=request.user,
                place=place,
                comment_text=form.cleaned_data['comment_text'],
                start_give=form.cleaned_data['start_give'],
            )
            return redirect(reverse('product:product_view', kwargs={'id': place.id}))
        
        return render(request, 'product/detail.html', context={'kitob': place, 'form': form, 'a': start_give})



def Cart(request, id):
    category = get_object_or_404(Catigory, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'product/detail_category.html', context={'category': category, 'products': products})

class AddKitobView(View):
    def get(self, request):
        form = AddKitob(request=request)
        return render(request, 'product/addkitob.html', context={'form': form})

    def post(self, request):
        form = AddKitob(request.POST, request.FILES,request=request)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('product:home')
        return render(request, 'product/addkitob.html', context={'form': form})
    
class AddTilView(View):
    def get(self,request):
        form=AddTilForm()
        return render(request,'product/addtil.html',context={'form':form})
    def post(self,request):
        if request.method=='POST':
            form=AddTilForm(data=request.POST,files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('product:home')
        return render(request,'product/addtil.html',context={'form':form})


class UpdatePlace(View):
    def get(self, request, pk):
        place_instance = Product.objects.get(id=pk)
        form = AddKitob(instance=place_instance)
        return render(request, 'product/update.html', context={'form': form})
    
    def post(self, request,pk):
        place_instance = Product.objects.get(id=pk)
        form = AddKitob(instance=place_instance, data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Muvaffaqiyatli o'zgartirildi")
            return redirect('product:home') 
        return render(request, 'product/update.html', context={'forms': form})
    
def delete(request, pk):
    place_instance = get_object_or_404(Product, id=pk)
    place_instance.delete()
    return redirect('product:home')


def cart_add(request):
    cart=Cart_Product(request)

    print(request.POST)
    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))
        quentity=request.POST.get('product_quentity')
        product=get_object_or_404(Product,id=product_id)
        cart.add(product=product,quentity=quentity)
        
        # print(product.id)
        return JsonResponse({'product_id':product_id})
    return HttpResponse("Hello world")

# def cart_tasdiqlash(request):
#     cart = Cart_Product(request)
#     if request.method == 'POST' and request.POST.get('action') == 'post':
#         product_quantity = request.POST.get('product_quantity')
#         total = request.POST.get('product_total')
#         product_price = request.POST.get('product_price')

#         product_ids = request.POST.getlist('product_ids')  # Ensure this matches the form field name

#         try:
#             product_quantity = product_quantity
#             total = float(total)
#             product_price = float(product_price)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid input data'}, status=400)

#         products = Product.objects.filter(id__in=product_ids)
        
#         cart.save(product=products, product_quantity=product_quantity, total=total, product_price=product_price)
        
#         return JsonResponse({'product_id': 'salom'})
#     return HttpResponse("Hello world")
        
        
def cart_summery(request):
    cart = Cart_Product(request)
    products = cart.get_products()
    quantities = cart.get_quantity()
    price = cart.get_total()
    all_products=cart.get_all_info()
    
    context = {
        'products': products,
        'quantities': quantities,
        'price': price,
        'all_products': all_products,
    }

    return render(request, 'product/cart_summery.html', context=context)


# def cart_update(request):
#     cart=Cart_Product(request)
#     print(request.POST)
#     if request.POST.get('action')=='post':
#         product_id=request.POST.get('product_id')
#         quantity=request.POST.get('product_quentity')
#         product=get_object_or_404(Product,pk=product_id)
#         cart.product_update(product=product,quantity=quantity)
#         return JsonResponse({"salom":"salom"}) 
#     return HttpResponse("Hello word") 

def cart_update_plus(request):
    cart=Cart_Product(request)
    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))
        quentity=request.POST.get('product_quentity')
        product=get_object_or_404(Product,pk=product_id)

        cart.product_plus(product,quentity)
        
    return JsonResponse({"salom":"salom"})
    # return render(request,"product/cart_summery.html")
    

def cart_update_remove(request):
    cart=Cart_Product(request)
    if request.POST.get('action')=='post':
        product_id=request.POST.get('product_id')
        quentity=request.POST.get('product_quentity')
        product=get_object_or_404(Product,pk=product_id)

        cart.product_remove(product,quentity)
        
    return JsonResponse({'salom':'salom'})

def cart_delete(request):
    if request.POST.get('action')=='post':
        cart =Cart_Product(request) 
        product_id=request.POST.get('product_id')
        cart.delete_product(product_id)
        return JsonResponse({"salom":"salom"}) 


# malumotlar omboriga saqlash
# telegram botga xabar yuborish

# views.py
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from .models import Order, OrderItem
import uuid

class OrderView(View):
    def post(self, request):
        cart = Cart_Product(request)
        all_orders = cart.get_all_info()
        total = cart.get_total()

        data = {
            'all_orders': all_orders,
            'total': total,
        }
        
        try:
            # Create and validate Order instance
            order = Order(
                order_id=uuid.uuid4(),
                total_price=total,
                user=request.user
            )
            
            order.save()

        except ValidationError as e:
            print(f"Order model validation error: {e.message_dict}")
            raise ValidationError("Order modeliga saqlashda xatolik")
        except Exception as e:
            print(f"Unexpected error when saving Order: {e}")
            raise ValidationError("Order modeliga saqlashda xatolik")

        try:
            # Create and validate each OrderItem instance
            for item in all_orders:
                order_item = OrderItem(
                    order=order,
                    product_id=item['id'],
                    price=item['price'],
                    name=item['name'],
                    quantity=item['quantity']
                )
               
                order_item.save()

        except ValidationError as e:
            print(f"OrderItem model validation error: {e.message_dict}")
            raise ValidationError("OrderItem modeliga saqlashda xatolik")
        except Exception as e:
            print(f"Unexpected error when saving OrderItem: {e}")
            raise ValidationError("OrderItem modeliga saqlashda xatolik")

        cart.clear_cart()

        return render(request, 'product/check.html', context=data)

class History(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        orders=user.orders.all()
        date={
            "orders":orders
        }
        return render(request,'product/order.html',context=date)
        

