from django.urls import path
from .views import Index,Login,Signup,Cart,logout,OrderView,success,payment,handlerequest,checkout
from .middlewares.auth import auth_middleware
# from .views import razorpaycheck
urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('Login',Login.as_view(),name='Login'),
    path('logout',logout,name='Logout'),
    path('success/',success,name='success'),
    path('payment',payment,name='payment'),
    path('signup',Signup.as_view(),name='signup'),
    path('cart',auth_middleware(Cart),name='cart'),
    path('checkout', checkout , name='checkout'),
    # path('Checkout', Checkout.as_view() , name='Checkout'),
    # path('/proceed-to-pay',razorpaycheck ),
    path('orders',auth_middleware( OrderView.as_view()), name='orders'),
    path('handlerequest',handlerequest, name = 'handlerequest'),
]