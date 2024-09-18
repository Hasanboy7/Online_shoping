from .models import Product
class   Cart_Product:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quentity):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = str(quentity)
        
        self.session.modified = True
    def product_plus(self,product,quentity):
        product_id=str(product.id)
        quantity=int(quentity)
        # self.cart[product_id]=quentity
        self.cart[product_id] = str(quentity)
        self.session.modified = True
        cart=self.cart
        return cart 
    
    def product_remove(self,product,quentity):
        product_id=str(product.id)
        quentity=int(quentity)
        self.cart[product_id]=quentity
        self.session.modified = True
        cart=self.cart
        return cart 

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantity(self):
        return self.cart
    
    def get_total(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)

        total=0

        for key,value in self.cart.items():
            key=int(key)
            for product in products:
                if product.id==key:
                    total=total+(int(product.price)*int(value))
        
        return total


    def delete_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

   
    
    def get_all_info(self):
        products=self.get_products()
        
        result=[]
        for product in products:
            if str(product.id) in self.cart:
                data={
                    "id":str(product.id),
                    "name":product.name,
                    "price":product.price,
                    "quantity":str(self.cart[str(product.id)]),
                    "jami":str(int(product.price)*int(self.cart[str(product.id)]))
                }
                result.append(data)
        return result
            
    def clear_cart(self):
        self.cart.clear()
        self.session.modified = True
        return True 

        
    # def save(self, product, product_quantity, total, product_price):
    #     product_quantity = int(product_quantity)
    #     total = float(total)
    #     product_price = float(product_price)

    #     for item in product:
    #         product_id = str(item.id)
    #         if product_id in self.cart:
    #             self.cart[product_id]['quantity'] = product_quantity
    #             self.cart[product_id]['total'] = total
    #             self.cart[product_id]['product_price'] = product_price
    #         else:
    #             self.cart[product_id] = {
    #                 'quantity': product_quantity,
    #                 'total': total,
    #                 'product_price': product_price
    #             }
    #     self.session['session_key'] = self.cart
    #     self.session.modified = True
        
    #     return self.cart
