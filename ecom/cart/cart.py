class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product , quantity = 1 , size = None):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': quantity , 'size' : size}  
        self.session.modified = True
        
    def get_total_price(self):
        total = 0
        for item in self.cart.values():
            total += float(item['price']) * item['quantity']
        return total

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())  
