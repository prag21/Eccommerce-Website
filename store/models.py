
from django.db import models
import datetime



class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    def get1():
        return Category.objects.all()

class Products(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    description=models.CharField(max_length=200,default='')
    image=models.ImageField(upload_to='pics')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    @staticmethod
    def get_product_by_id(id):
        return Products.objects.filter(id__in=id)
    def get3(id):
        return Products.objects.get(id=id)
    def get():
        return Products.objects.all()
    @staticmethod
    def get2(category_id):
        if category_id:
            return Products.objects.filter(category_id=category_id)
        else:
            return Products.objects.all()
class Customers(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=100)
    def register(self):
        self.save()
    def isexist(self):
        if Customers.objects.filter(email = self.email):
            return True
        return False
    def get(email,password):
        try:
            return Customers.objects.get(email=email,password=password)
        except:
            return False
    def get1(email):
        return Customers.objects.get(email=email)
class Order(models.Model):
    productid=models.ForeignKey(Products,on_delete=models.CASCADE)
    customerid=models.ForeignKey(Customers,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)

    def register(self):
        self.save()
    def get_order(id):
        return Order.objects.filter(customerid=id).order_by('-date')
class Cart(models.Model):
    productid=models.ForeignKey(Products,on_delete=models.CASCADE)
    customerid=models.ForeignKey(Customers,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    def get_customer(id1):
        return Cart.objects.filter(customerid=id1)
    def get_cust(id2):
        return Cart.objects.filter(customerid=id2)
    def get_p_c(id1,id2):
        try:
            return Cart.objects.get(productid=id1,customerid=id2)
        except:
            return False


    




