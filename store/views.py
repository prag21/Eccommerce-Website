from fresh.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from django.http.response import HttpResponseRedirect

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from .import models
from django.views import View
from store.middlesware.auth import auth_middleware

import razorpay


class home(View):
    def get(self,request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        p=None 
        c=models.Category.get1()
        ce=request.GET.get('category_id')
        if ce:
            p=models.Products.get2(ce)
        else:
            p=models.Products.get()
        data={}
        data['p']=p
        data['c']=c
        return render(request,'index.html',data)
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cust=request.session.get('id')
        p=models.Products.get3(product)
        q1=models.Cart.get_p_c(product,cust)
        if q1:
            q=q1.quantity
            if q :
                if remove:
                    if q<=1:
                       
                        q1.delete()
                    else:
                       
                        q1.quantity=q1.quantity-1
                        q1.save()
                     
         
                        
                    
                else:
                   
                    q1.quantity=q1.quantity+1
                    q1.save()
             
         
                   
                 
                
                 
            else:
               
                q1.quantity=1
                q1.save()
    
         
              
             
                
        else:
           
            c1=models.Cart(customerid=models.Customers(id=cust),productid=models.Products(id=product),price=p.price,quantity=1)
            c1.save()
            
            
          
        
 

        return redirect('home')
  


class sign(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        value={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email,
        }
        customer=models.Customers(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
        #validation
        error=None
        if (not first_name):
            error='First Name required'
        elif len(first_name)<4:
            error="Not Valid"
        if (not last_name):
            error='First Name required'
        elif len(last_name)<4:
            error="Not Valid"
        if (not phone):
            error='Phone required'
        elif len(phone)<5:
            error='Phone Number not valid'
        if (not password):
            error='Password required'
        if customer.isexist():
             error="Exitsts"
        
        if not error:
    
            
            customer.register()
            return redirect('home') 
        else:
 
            return render(request,'signup.html',{'error':error,'value':value})
       

      
class login(View):
    return_Url=None
    def get(self,request):
        login.return_Url=request.GET.get('return_Url')
        return render(request,'login.html')
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=models.Customers.get(email,password)
        error=None 
        if customer:
            request.session['id']=customer.id
            request.session['email']=customer.email
            if login.return_Url:
                return HttpResponseRedirect(login.return_Url)
            else:
                login.return_Url=None
                return redirect('home')
        else:
            error="Email or Password invalid"
            return render(request,'login.html',{'error':error})

def logout(request):
    request.session.clear()
    return redirect('login')  
class cart(View):
    def get(self,request):
        cust=request.session.get('id')
        i=models.Cart.get_cust(cust)
        l=[]
        for i1 in i:
            l.append(i1.productid)
        return render(request,'cart.html',{'p':l})

class checkout(View):
    def get(self,request):
        return render(request,'chechkout.html')
    def post(self,request):
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        cust=request.session.get('id')
        cart=models.Cart.get_cust(cust)
        l=[]
        l1=[]
        for i1 in cart:
            l.append(i1.productid)
        for i2 in l:
            l1.append(i2.id)
        products=models.Products.get_product_by_id(l1)
        total=0
        for p in products:
            c=models.Cart.get_p_c(p,cust)
            total+=c.quantity*p.price
            o=models.Order(customerid=models.Customers(id=cust),productid=p,price=p.price,quantity=c.quantity,address=address,phone=phone)
            o.register()
        c=models.Cart.get_cust(cust)
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        order_currency = 'INR'
        order_amount = total
        if order_amount>100:
            payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1))
            payment_order_id=payment_order['id']
            i=request.session.get('email')
            o=models.Customers.get1(i)
            context={'amount':total,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id,'email':o.email,'id':o.first_name}
            return render(request,'payment.html',context)
        c.delete()
        return redirect('cart')

class order(View):
    def get(self,request):
        customer=request.session.get('id')
        orders=models.Order.get_order(customer)
        return render(request,'order.html',{'order':orders})









       