from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from agents.models import Accociate
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    if request.method == "POST":
        loginusername = request.POST['username']
        loginpassword = request.POST["password"]

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            dj_login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('/franchise')
        else:
            messages.error(request, "Invaild Credentials, Please try again")
            return redirect('/franchise/login')
    return render(request, "franchise/pages/login.html")


@login_required
def franchisePage(request):
    user = User.objects.get(username=request.user)
    kit = Franchise.objects.get(user=user)
    recent_activations = activationHistory.objects.filter(supplier=kit)
    context = {
        "kit":kit,
        "recent_activations":recent_activations
    }
    return render(request, "franchise/pages/franchise.html", context)

@login_required
def sellKit(request):
    if request.method == "POST":
        _userid = request.POST['user']
        user = User.objects.get(username=_userid)
        accociate = Accociate.objects.get(user=user)
        accociate.is_active = True
        accociate.save()
        current_user = User.objects.get(username=request.user)
        print(current_user)
        supplier = Franchise.objects.get(user=current_user)
        supplier.available_kits -= 1
        supplier.save()

        new = activationHistory.objects.create(supplier=supplier, user=accociate)
        new.save()
    userid = request.GET['username']
    user = User.objects.get(username=userid)
    if user is None:
        messages.warning(request, 'User Not Found.')
    accociate = Accociate.objects.get(user=user)

    context = {"accociate":accociate}

    return render(request, 'franchise/pages/user-details.html', context)

@login_required
def purchaseHistory(request):
    user = User.objects.get(username=request.user)
    supplier = Franchise.objects.get(user=user)
    history = Sell.objects.filter(supplier=supplier)
    context = {
        "history":history
    }
    return render(request, "franchise/pages/purchase.html", context)

@login_required
def sellHistory(request):
    user = User.objects.get(username=request.user)
    supplier = Franchise.objects.get(user=user)
    history = activationHistory.objects.filter(supplier=supplier)
    context = {
        "history":history
    }
    return render(request, "franchise/pages/sell.html", context)
    
    
@login_required
def repurchase(request):
    user = User.objects.get(username=request.user)
    supplier = Franchise.objects.get(user=user)
    products = RepurchaseProduct.objects.filter(franchise=supplier)
    context = {
        "products":products
    }
    return render(request, 'repurchase/pages/repurchase.html', context)



@login_required
def sellProduct(request):
    if request.method == 'POST':

        # getting data from client
        supplier_user = User.objects.get(username=request.user)
        supplier = Franchise.objects.get(user=supplier_user)
        _userid = request.POST['user']
        user = User.objects.get(username=_userid)
        accociate = Accociate.objects.get(user=user)
        product_list = request.POST.getlist('product[]')
        quantity_list = request.POST.getlist('quantity[]')


        # Process the form data for multiple RepurchaseSell objects
        for product, quantity in zip(product_list, quantity_list):
            if product and quantity:
                # Get or create RepurchaseProduct
                qtt, created = RepurchaseProduct.objects.get_or_create(franchise=supplier, product=product)

                # Update quantity
                if qtt.quantity >= int(quantity) and int(quantity) != 0:
                    qtt.quantity -= int(quantity)
                    qtt.save()
                else:
                    messages.warning(request, "Out of Stcok")    

                prod = Product.objects.get(id=product)
                # Create RepurchaseSellHistory
                RepurchaseSellHistory.objects.create(supplier=supplier, user=accociate, product=prod, quantity=quantity)

                

    
    userid = request.GET['username']
    user = User.objects.get(username=userid)
    if user is None:
        messages.warning(request, 'User Not Found.')
    accociate = Accociate.objects.get(user=user)

    product = Product.objects.all()
    context = {"accociate":accociate, "products":product}

    return render(request, 'repurchase/pages/user-details.html', context)


def repurchasePurchaseHistory(request):
    user = User.objects.get(username=request.user)
    supplier = Franchise.objects.get(user=user)
    sells = Sell.objects.filter(supplier=supplier)
    history = RepurchaseSell.objects.filter(sell__in=sells)
    context = {
        "history": history
    }
    return render(request, "repurchase/pages/purchase.html", context)



def repurchaseSellHistory(request):
    user = User.objects.get(username=request.user)
    supplier = Franchise.objects.get(user=user)
    history = RepurchaseSellHistory.objects.filter(supplier=supplier)
    context = {
        "history":history
    }
    return render(request, "repurchase/pages/sell.html", context)    
    
    