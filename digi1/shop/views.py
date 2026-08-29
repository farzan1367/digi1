from importlib.metadata import requires
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from  django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.db import transaction
from .forms import SignUpForm ,UpdateUserForm,UpdatePasswordForm,UpdateUserInfo
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress,Order,OrderItem
from .models import Product,Category,Profile,ProductMedia

import json

# =========================================================
# Upload Product Media
# =========================================================

@require_POST
def upload_product_media(request, product_id):
    if not request.user.is_staff:
        return JsonResponse(
            {
                "success": False,
                "message": "Permission Denied."
            },
            status=403
        )
    product = get_object_or_404(Product, id=product_id)

    files = request.FILES.getlist('files')

    if not files:
        return JsonResponse({
            'success': False,
            'message': 'No files selected.'
        }, status=400)

    last_media = (
        ProductMedia.objects
        .filter(product=product)
        .order_by('-sort_order')
        .first()
    )

    next_order = last_media.sort_order + 1 if last_media else 0

    media_objects = []

    for index, file in enumerate(files):

        if file.content_type.startswith('image/'):
            media_type = 'image'

        elif file.content_type.startswith('video/'):
            media_type = 'video'

        else:
            continue

        media_objects.append(
            ProductMedia(
                product=product,
                file=file,
                media_type=media_type,
                sort_order=next_order + index,
            )
        )

    ProductMedia.objects.bulk_create(media_objects)

    return JsonResponse({
        'success': True,
        'count': len(media_objects),
    })

# =========================================================
# Delete Product Media
# =========================================================

@require_POST
def delete_product_media(request, product_id,media_id):
    if not request.user.is_staff:
        return JsonResponse(
            {
                'success': False,
                'message': 'Permission Denied.'
            },
            status=403
        )
    product = get_object_or_404(Product, id=product_id)
    media = get_object_or_404(ProductMedia, id=media_id,product=product)

    if media.file:
        media.file.delete(save=False)
    media.delete()

    # مرتب‌سازی مجدد sort_order
    remaining_media = ProductMedia.objects.filter(product=product).order_by('sort_order','id')
    for index,item  in enumerate(remaining_media):
        if item.sort_order != index:
            item.sort_order = index
            item.save(update_fields=['sort_order'])
    return JsonResponse({
        'success': True,
        'count': 'Media deleted.',
    })

# =========================================================
# Reorder Product Media
# =========================================================

@require_POST
def reorder_product_media(request, product_id):

    if not request.user.is_staff:
        return JsonResponse(
            {
                'success': False,
                'message': 'Permission Denied.'
            },
            status=403
        )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    try:
        data = json.loads(request.body)
        media_ids = data.get('order', [])

    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid JSON.'
            },
            status=400
        )

    if not isinstance(media_ids, list):
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid order data.'
            },
            status=400
        )

    try:
        media_ids = [int(media_id) for media_id in media_ids]
    except (TypeError, ValueError):
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid media IDs.'
            },
            status=400
        )

    media_objects = list(
        ProductMedia.objects.filter(
            product=product,
            id__in=media_ids
        )
    )

    if len(media_objects) != len(media_ids):
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid media IDs.'
            },
            status=400
        )

    media_map = {
        media.id: media
        for media in media_objects
    }

    with transaction.atomic():

        for index, media_id in enumerate(media_ids):
            media = media_map[media_id]
            media.sort_order = index

        ProductMedia.objects.bulk_update(
            media_objects,
            ['sort_order']
        )

    return JsonResponse(
        {
            'success': True,
            'message': 'Order updated successfully.'
        }
    )


# =========================================================
# Product List
# =========================================================
class ProductListView(ListView): #def helloworld
    model = Product
    context_object_name = 'products'
    paginate_by =20
    template_name = 'index.html'

# def helloworld(request):
#     all_products=Product.objects.all()
#     return render(request,"index.html",{"products":all_products})

# =========================================================
# Product Detail
# =========================================================
class ProductDetailView(DetailView): #def product
    model = Product
    context_object_name = 'product'
    template_name = 'product.html'

# def product(request,pk):
#     product=Product.objects.get(id=pk)
#     return render(request,"product.html",{"product":product})

# =========================================================
# Category List
# =========================================================
class CategoryListView(ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_summary.html'

# def category_summary(request):
#     all_cat=Category.objects.all()
#     return render(request,"category_summary.html",{'category':all_cat})

# =========================================================
# Category Detail
# =========================================================
class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'category.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    # def get_object(self):
    #     cat = self.kwargs.get("cat").replace("-", " ")
    #     return get_object_or_404(Category,name=cat)
        # return Category.objects.get(name=cat)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category = self.object
    #
    #     context['products'] = Product.objects.filter(category=category)
    #     return context

# def category(request,cat):
#     cat = cat.replace("-", " ")
#     try:
#         category=Category.objects.get(name=cat)
#         #category=Category.objects.get(id=cat)
#         products=Product.objects.filter(category=category)
#         return render(request,"category.html",{"products":products,"category":category})
#     except:
#         messages.success(request,("دسته بندی مورد نظر وجود ندارد"))
#         return redirect ("home")


# =========================================================
# Order Details
# =========================================================
def order_details(request,pk):
    if request.user.is_authenticated:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)

        context ={
            'order':order,
            'items':items
        }

        return render(request,'order_details.html',context)
    else:
        messages.success(request,'شما اجازه دسترسی ندارید')
        return redirect('home') 
    

def user_orders(request):
    if request.user.is_authenticated:
        delivered_order = Order.objects.filter(user=request.user,status='Delivred')
        other_order = Order.objects.filter(user=request.user).exclude(status='Delivred')
        context ={
            'delivered':delivered_order,
            'other':other_order
        }

        return render(request,'orders.html',context)
    else:
        messages.success(request,'شما اجازه دسترسی ندارید')
        return redirect('home')    


def search(request):
    if request.method =='POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request,'چنین محصولی وجود ندارد')
            return redirect('search')
        else:
            return render(request,'search.html',{'searched':searched})
    return render(request,'search.html',{})    


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UpdateUserInfo(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,'اطلاعات کاربری شما ویرایش شد')
            return redirect('home')

        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form}) 
    else:
        messages.success(request,'ابتدا باید لاگین شوید')  
        return redirect('login') 





def about(request):
    return render(request,'about.html')    

def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request,user)
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                cart = Cart(request)
                convert_cart = json.loads(saved_cart)
                for key,value in convert_cart.items():
                    cart.db_add(product=key,quantity=value)
                    

            messages.success(request,("با موفقیت وارد شدید"))
            return redirect ("home")
        else:
            messages.success(request,(" مشکلی در وارد شدن وجود داشت"))
            return redirect ("login")

    else:    
        return render(request,'login.html') 
    

def logout_user(request):
    logout(request)
    messages.success(request,("با موفقیت خارج شدید"))
    return redirect("home")

def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user=authenticate(request,username=username,password=password1)
            login(request,user)
            messages.success(request,("ثبت نام شما با موفقیت انجام شد"))
            return redirect ("update_info")
        else:
            for err in list(form.errors.values()):
                messages.error(request,err)
            messages.success(request,(" مشکلی در ثبت نام وجود دارد"))
            return redirect ("signup")   
    else:
        return render(request,"signup.html",{'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance = current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,'پروفایل شما ویرایش شد')
            return redirect('home')

        return render(request,'update_user.html',{'user_form':user_form}) 
    else:
        messages.success(request,'ابتدا باید لاگین شوید')  
        return redirect('login') 
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user 

        if request.method == "POST":
            form  = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request,current_user)
                messages.success(request,'رمز با موفقیت ویرایش شد')
                return redirect('update_user') 
            else:
                for err in list(form.errors.values()):
                    messages.error(request,err)
                return redirect('update_password')    
        else:
            form = UpdatePasswordForm(current_user)            
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,'لطفا ابتدا وارد شوید')
        return redirect('login') 



