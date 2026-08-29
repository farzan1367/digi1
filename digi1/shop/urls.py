
from django.urls import path,include
from . import views
from .views import ProductListView,ProductDetailView,CategoryListView,CategoryDetailView

urlpatterns = [
    path('',ProductListView.as_view(),name='home'),
    # path('',views.helloworld ,name="home"),
    path('about/',views.about, name="about"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('signup/',views.signup_user, name="signup"),
    path('update_user/',views.update_user, name="update_user"),
    path('update_info/',views.update_info, name="update_info"),
    path('update_password/',views.update_password, name="update_password"),
    path('product/<int:pk>',ProductDetailView.as_view(), name="product"),
    path('category/<str:slug>',CategoryDetailView.as_view(), name="category"),
    #path('category/<int:cat>',views.category, name="category"),
    path('category/',CategoryListView.as_view(), name="category_summary"),
    path('search/',views.search, name="search"),
    path('orders/',views.user_orders, name="orders"),
    path('order_details/<int:pk>',views.order_details, name="order_details"),
    path(
        'product/<int:product_id>/upload_media/',
        views.upload_product_media,
        name="upload_product_media"
    ),
   
]