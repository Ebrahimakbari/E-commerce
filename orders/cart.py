CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self):
        for item in self.cart.values():
            yield item
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_price = str(product.price)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {'quantity':0, 'price':product_price, 'total_price':0}
        self.cart[product_id]['quantity'] += quantity
        self.cart[product_id]['total_price'] = str(self.cart[product_id]['quantity'] * int(product_price))
        self.cart[product_id]['product'] = product.name
        self.cart[product_id]['slug'] = product.slug
        self.cart[product_id]['pk'] = product.pk
    
    def remove(self, product_id):
        value = self.cart.get(str(product_id))
        if value:
            del self.cart[str(product_id)]
            return True
        return False
            
    
    def save(self):
        self.session.modified = True
    
    def get_cart_total_price(self):
        return sum(int(item['total_price']) for item in self.cart.values())