from django.shortcuts import render,redirect,get_object_or_404
from cart.cart import Cart
from .models import ShippingAddress,Order,OrderItem
from .forms import ShippingForm
from django.contrib import messages
from shop.models import Product,Profile
from django .contrib.auth.models import User

def payment_success(request):
    return render(request,'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities =cart.get_quants()
    total = cart.get_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_form':shipping_form })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request,"payment/checkout.html",{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_form':shipping_form })
    
def confirm_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities =cart.get_quants()
        total = cart.get_total()

        if request.user.is_authenticated:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            if shipping_form.is_valid():
                shipping_form.save()

        user_shipping = request.POST
        request.session['user_shipping'] = user_shipping        
        return render(request,"payment/confirm_order.html",{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_info':user_shipping })
    
    else:
        messages.success(request,'دسترسی به این صفحه امکان پذیر نمی باشد')
        return redirect('home')

    return render(request,'payment/confirm_order.html')    

def proccess_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities =cart.get_quants()
        total = cart.get_total()

        user_shipping = request.session['user_shipping']
        full_name = user_shipping['shipping_full_name']
        email= user_shipping['shipping_email']
        full_address = f'{user_shipping['shipping_adress1']}\n {user_shipping['shipping_adress2']}\n شهر:{user_shipping['shipping_city']}\n منطقه:{user_shipping['shipping_state']}\n کدپستی:{user_shipping['shipping_zipcode']}\n کشور:{user_shipping['shipping_country']}'

        if request.user.is_authenticated:
            user = request.user 
            new_order = Order(
                user = user,
                full_name = full_name,
                email = email,
                shipping_adress = full_address,
                amount_paid = total
            )
            new_order.save()
            odr = get_object_or_404(Order,id=new_order.pk)

            for product in cart_products:
                prod = get_object_or_404(Product,id=product.id)

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities.items():
                    if int(key) == product.id:
                        new_item = OrderItem(
                            order = odr,
                            product = prod,
                            price = price,
                            quantity = value,
                            user = user
                        )
                        new_item.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]  

            cu = Profile.objects.filter(user__id=request.user.id)
            cu.update(old_cart="")              

            messages.success(request,'سفارش شما ثبت شد')
            return redirect('home')
        else:
            new_order = Order(
                full_name = full_name,
                email = email,
                shipping_adress = full_address,
                amount_paid = total
            )
            new_order.save()
            odr = get_object_or_404(Order,id=new_order.pk)

            for product in cart_products:
                prod = get_object_or_404(Product,id=product.id)

                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities.items():
                    if int(key) == product.id:
                        new_item = OrderItem(
                            order = odr,
                            product = prod,
                            price = price,
                            quantity = value,
                            
                        )
                        new_item.save()
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]  
            messages.success(request,'سفارش شما ثبت شد')
            return redirect('home')
    else:
        messages.success(request,'دسترسی به این صفحه امکان پذیر نمی باشد')
        return redirect('home')        
