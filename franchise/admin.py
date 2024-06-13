from django.contrib import admin
from .models import *

# Register your models here.
class RepurchaseProductInline(admin.TabularInline):
    model = RepurchaseProduct
    extra = 1


class activationAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'user', 'activation_time']

class RepurchaseSellInline(admin.TabularInline):
    model = RepurchaseSell
    extra = 1
    # readonly_fields = ['product']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'DP', 'BV']

class FranchiseAdmin(admin.ModelAdmin):
    inlines = [RepurchaseProductInline]    
    extra = 1 
    readonly_fields = ['available_kits',]

class SellAdmin(admin.ModelAdmin):
    inlines = [RepurchaseSellInline,]    

class RPSH(admin.ModelAdmin):
    list_display = ['supplier', 'user', 'product', 'quantity', 'created_at']
    list_filter = ['supplier', 'user', 'product', 'created_at']


admin.site.register(Franchise, FranchiseAdmin)
admin.site.register(Sell, SellAdmin)
admin.site.register(activationHistory, activationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(RepurchaseSellHistory, RPSH)