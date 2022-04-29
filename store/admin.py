from django.contrib import admin
from .models import Category, Customers, Products,Order

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category']
class AdminCategory(admin.ModelAdmin):
     list_display=['name']

admin.site.register(Products,AdminProduct)
admin.site.register(Category,AdminCategory)
admin.site.register(Customers)
admin.site.register(Order)