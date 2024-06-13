from django.db import models
from django.contrib.auth.models import User
from agents.models import Accociate
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Franchise(models.Model):
    id = models.AutoField(primary_key=True)
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.TextField()
    gstin = models.CharField(max_length=250)
    available_kits = models.PositiveIntegerField(null=True, blank=True, default=0)

    
    def __str__(self):
        return self.name
    
class Sell(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    kit = models.PositiveIntegerField()
    MRP = models.PositiveIntegerField()
    DP = models.PositiveIntegerField()
    BV = models.PositiveIntegerField()

    def __str__(self):
        return str(self.supplier)
    

    def save(self, *args, **kwargs):
        # Calculate the number of kits being sold
        num_kits_sold = self.kit

        # Update the available kits for the supplier (Franchise)
        self.supplier.available_kits += num_kits_sold
        self.supplier.save()

        super(Sell, self).save(*args, **kwargs)

        
class activationHistory(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    user = models.ForeignKey(Accociate, on_delete=models.CASCADE)
    activation_time = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.supplier)
        
        
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    DP = models.PositiveIntegerField()
    BV = models.PositiveIntegerField()


    def __str__(self):
        return self.name


class RepurchaseProduct(models.Model):
    id = models.AutoField(primary_key=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)


class RepurchaseSell(models.Model):
    id = models.AutoField(primary_key=True)
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.quantity)



@receiver(post_save, sender=RepurchaseSell)
def update_repurchase_product_quantity(sender, instance, created, **kwargs):
    if created:
        repurchase_product = RepurchaseProduct.objects.filter(
            franchise=instance.sell.supplier,
            product=instance.product
        ).first()

        if repurchase_product:
            # Update the quantity in RepurchaseProduct
            repurchase_product.quantity += instance.quantity
            repurchase_product.save()
        else:
            # Create a new RepurchaseProduct entry
            RepurchaseProduct.objects.create(
                franchise=instance.sell.supplier,
                product=instance.product,
                quantity=instance.quantity
            )

class RepurchaseSellHistory(models.Model):
    id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    user = models.ForeignKey(Accociate, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.supplier)        
        
    