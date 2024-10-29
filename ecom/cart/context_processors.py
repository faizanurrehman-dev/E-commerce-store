from .cart import Cart

def cart(request):
    return {'cart_quantity': Cart(request).get_total_quantity()}
