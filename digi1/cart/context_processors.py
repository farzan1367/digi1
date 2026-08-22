from .cart import Cart
from shop.models import Category

def cart(request):
    return {'cart':Cart(request)}

def cateqory(request):
    categories=Category.objects.all()
    return ({'categories':categories})