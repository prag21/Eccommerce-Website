from django.http import request
from store import models
from django import template

register = template.Library()





@register.filter(name='is_in_cart1')
def is_in_cart1(p1,cust):
    c=models.Cart.get_p_c(p1,cust)
    if c:
        return True
    else:
        return False
@register.filter(name='get_quantity')
def get_quantity(p1,cust):
    c=models.Cart.get_p_c(p1,cust)
    if c:
        return c.quantity
    else:
        return 0




@register.filter(name='total1')
def total1(p1,cust):
    return p1.price * get_quantity(p1,cust)
    return 0
@register.filter(name='totali1')
def totali1(p1,cust):
    sum=0
    for p in p1:
        sum+=total1(p,cust)
    return sum


  



