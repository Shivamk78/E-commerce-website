from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
# Create your views here.

class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        print('*************')
        # id=request.session['customer']
        # c=Customer.objects.filter(id)
        # print(c)
        print('this is cart value', cart)
        print('*************')
        if not cart:
            request.session['cart'] = {}
        product = Product.objects.all()
        context = {'product': product}
        # print('you are : ',request.session.get('email'))
        # messages.success(request,'this is test message')
        return render(request, 'index.html', context)

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print('product',product,'remove',remove,'cart',type(cart),cart)
        # for contact
        # name=request.POST.get('name')
        # email=request.POST.get('emaill')
        # subject=request.POST.get('subject')
        # message=request.POST.get('message')

        # contact=Contact(name=name, email=email, subject=subject, message=message)
        # contact.save()
        # messages.success(request, "Your message has been send.")

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('**************               ****************', request.session['cart'])
        return redirect('index')


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self, request):
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                name = customer.first_name

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    messages.success(
                        request, f'you are successful Login {name}')
                    return redirect('index')
            else:
                error_message = 'Email and Password invalid !!'
        else:
            error_message = 'Email and Password invalid !!'
        print(customer)
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name,
                            phone=phone, email=email, password=password)

        error_message = self.validateCustomer(customer)
        if not error_message:
            print(first_name, last_name, phone, email, password)

            subject = 'welcome to our website '
            message = f'Hi {customer.first_name}, thank you for registering in MILATOS.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [customer.email, ]
            send_mail(subject, message, email_from,
                      recipient_list, fail_silently=False)

            customer.password = make_password(customer.password)
            customer.register()
            messages.success(
                request, f'you are successful signup {first_name}')
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = 'First Name Required !!'
        elif len(customer.first_name) < 1:
            error_message = 'please enter correct name'
        elif not customer.last_name:
            error_message = 'please enter last name'
        elif not customer.phone:
            error_message = 'please enter phone no.'
        elif not customer.password:
            error_message = 'please enter password'
        elif customer.isExist():
            error_message = 'Email Address Already Registered..'

        # saving
        return error_message



def Cart(request):
    # data=request.POST
    # print('CARTCARTCARTCARTCARTCARTCARTCARTCART',data)
    # if request.method=='GET':
    #     print('this iss get')
    #     global p,i
    #     ids = list(request.session.get('cart').keys())
    #     i = list(request.session.get('cart').keys())
    #     print('########################')
    #     print(ids)
    #     print('########################')
    #     products = Product.get_products_by_id(ids)
    #     p = Product.get_products_by_id(i)
    #     print('this cart product function ', products)
    #     return render(request, 'cart.html', {'products': products})
    if request.method=='POST':
        print('this is post request')
        amount=0
        # global p,i
        ids = list(request.session.get('cart').keys())
        # i = list(request.session.get('cart').keys())
        print('########################')
        print(ids)
        print('########################')
        products = Product.get_products_by_id(ids)
        # p = Product.get_products_by_id(i)
        address = request.POST.get('address')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        name = request.session.get('customer')
        pincode = request.POST.get('pincode')
        print('our new add is ************',address,state,phone,name,pincode)
        cart = request.session.get('cart')
        name = request.session.get('customer')
        products = Product.get_products_by_id(list(cart.keys()))
        for product in products:
            print(cart.get(str(product.id)))
            print(product)
            print(product.price)
            amount = product.price*cart.get(str(product.id))+amount
           
        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest"
        # order=Order.objects.filter(customer=name)
        # print('this sis order fields ',order)
        print(callback_url)
        # print('products-:  ',products)
        print('amount is ***********%%%%%%%',amount)
        client = razorpay.Client(
        auth=(settings.KEY, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create(
        {'amount':amount*100 , 'currency': 'INR', 'payment_capture': '1'})
        print('payment is ^^^^^^^^^^',payment['id'])
        for product in products:
            order = Order(razorpay_order_id=payment['id'], product=product, price=product.price,
                            address=address, phone=phone, quantity=cart.get(str(product.id)))
            order.save()
        # order.razorpay_order_id=payment['id']
        # print('after order is save' ,order)
        # order.save()
        context = {'payment': payment,'razorpay_key': settings.KEY,'amount':amount,'callback_url':callback_url,'products': products}
        # request.session['cart'] = {} 
        return render(request,'cart.html',context)
    else:
        HttpResponse('505 not found')




def checkout(request):
    if request.method=='POST':
        address = request.POST.get('address')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        name = request.session.get('customer')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print('&&&&&&&&&&&&&&&&&&&&&&',address,state,phone,name,pincode,cart,products)
        for product in products:
                order = Order(customer=name, product=product, price=product.price,
                            address=address, phone=phone, quantity=cart.get(str(product.id)))
                order.save()
        
    return render(request,'checkout.html')





@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id','')
        signature = request.POST.get('razorpay_signature','')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(products,type(products))
        print(cart,type(cart))
        print(products,type(products))

        for pro in products:
            print(pro.product_name)
            print(pro.price)
        order=Order.objects.filter(razorpay_order_id=order_id)
        for i in order:
            i.razorpay_payment_id = payment_id
            i.razorpay_signature = signature
            i.save()
        mail_subject = 'Recent Order Details'
        context_dict = {'products':products}
        # template = get_template('emailinvoice.html')
        # message  = template.render(context_dict)
        to_email ='kshivam7835@gmail.com'

        print('Email is **************** --------------',to_email)
        request.session['cart'] = {} 
        return HttpResponse('this is test program')

def payment(request):
    ids = list(request.session.get('cart').keys())
    print('########################')
    print('########################')
    products = Product.get_products_by_id(ids)
    print('this cart yhfyuhf function ', ids)
    return render(request, 'payment.html', {'products': ids})


class OrderView(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print('order view', orders)
        return render(request, 'orders.html', {'orders': orders})


def success(request):
    if request.method == 'POST':
        # order=Order.objects.get(status=False)
        # print(order)
        address=request.POST.get('shipping_address')
        name=request.POST.get('name')
        phone=request.POST.get('phone_no')
        state=request.POST.get('country-state')
        pincode=request.POST.get('shipping_pin')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, state, pincode, name,cart,products)

        for product in products:
            order = Order(customer=name, product=product, price=product.price,
                          address=address, phone=phone, quantity=cart.get(str(product.id)))
        order.save()

        request.session['cart'] = {}
        # a = request.POST
       # print('hello world',a)
    address=request.POST.get('shipping_address')
    print('address',address)
    return  HttpResponse('your payment is success')

# def cart(request):
#     product=Product.objects.all()
#     context={'product':product}
#     return render(request,'cart.html',context)


def logout(request):
    request.session.clear()
    messages.success(request, 'you are logout')
    return redirect('Login')

# def razorpaycheck(request):
#     cart = request.session.get('cart')
#     products = Product.get_products_by_id(list(cart.keys()))
#     amount = 0

#     for product in products:
#         print(cart.get(str(product.id)))
#         print(product)
#         print(product.price)
#         amount = product.price*cart.get(str(product.id))+amount

#     return JsonResponse({
#         'total_price':amount
#     })
