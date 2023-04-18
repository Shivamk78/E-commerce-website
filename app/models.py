from django.db import models
import datetime

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.email

    def register(self):
        self.save()
        
    @staticmethod
    def get_email(id):
        return Customer.objects.get(id=id)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def isExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def __str__(self):
        return self.product_name
from django.utils import timezone
payment=(('c','cash'),('o','online'))
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=50 ,default='',null=True, blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)

    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    
    def placeOrder(self):
        return self.save()
    
    def save(self,*args, **kwargs):
        if True:
            return super().save(*args, **kwargs)
            
    def __str__(self):
        return self.phone

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')


    # def total_price(self):
    #     price=[]

        # class Contact(models.Model):
        #     name=models.CharField(max_length=50,null=True,blank=True)
        #     email=models.EmailField(null=True)
        #     subject=models.CharField(max_length=500,null=True)
        #     message=models.TextField(null=True)

        #     def __str__(self):
        #         return self.email
