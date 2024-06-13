from django.shortcuts import render, redirect
# from customer.models import Customer, Sponsor
from django.core.mail import send_mail 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import random
import string

# Create your views here.

def index(request):
    # characters = string.ascii_letters + string.digits  # Letters and digits
    # unique_sponsor_id = ''.join(random.choice(characters) for _ in range(8))
    # print(unique_sponsor_id)
    return render(request, 'client/home/index.html')

def about(request):
    return render(request, 'client/home/about.html')

def products(request):
    return render(request, 'client/home/products.html')

def mission(request):
    return render(request, 'client/home/mission.html')

def faqs(request):
    return render(request, 'client/home/faqs.html')

def contact(request):
    return render(request, 'client/home/contact.html')

def login(request):
    if request.method == "POST":
        loginusername = request.POST['username']
        loginpassword = request.POST["password"]

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            dj_login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('/user')
        else:
            messages.error(request, "Invaild Credentials, Please try again")
            return redirect('/login')
    
    return render(request, 'client/home/login.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        sponser_id = request.POST['sponser_id']
        dob = request.POST['dob']
        aadhar_card = request.FILES['aadhar_card']
        profile_picture = request.FILES['profile_picture']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # check sponser_id
        sponsor = Sponsor.objects.get(sponsor=sponser_id)
        if not sponsor:
            messages.error(request, 'Sponsor id not found')
        
        # check password
        if password != cpassword:
            messages.error(request, "Password does not match.")
            return render(request, 'client/home/register.html')

        # check user
        if email:
            email_exist = User.objects.filter(email=email).exists()

            if email_exist:
                messages.warning(request, "Email is already taken.")
                return render(request, 'client/home/register.html')

        # Hash the password
        hashed_password = make_password(password)  # Use make_password to hash the password


        # create a sposnsor id 
        characters = string.ascii_letters + string.digits  # Letters and digits
        unique_sponsor_id = ''.join(random.choice(characters) for _ in range(8))


        # create customer
        customer = Customer.objects.create(name=name, phone=phone, email=email, sponsor=sponsor, own_sponsor_id=unique_sponsor_id, dob=dob, aadhar_card_image=aadhar_card, profile_picture=profile_picture, password=hashed_password)  # Use hashed_password
        customer.save()

        # create user
        user = User.objects.create(username=email, password=hashed_password, email=email, first_name=name)  # Use hashed_password
        user.save()

        

        # send success mail
        subject = "Greetings"
        msg = "Congratulations, Your account is successfully created."
        to = email
        res = send_mail(subject, msg, "suraj.juneco@gmail.com", [to])
        if res == 1:
            msg = "Mail Sent Successfully"
        else:
            msg = "Mail could not be sent"

        # login
        dj_login(request, user)


        make_sponsor_id = Sponsor.objects.create(sponsor=unique_sponsor_id, user=user)
        make_sponsor_id.save()


        # upgrade level 
        customer_count = Customer.objects.filter(sponsor=sponsor).count()

        if customer_count >= 4:
            customers_to_update = Customer.objects.filter(sponsor=sponsor) 
            for customer in customers_to_update:
                customer.level = 2
                customer.save()
            print(f"Updated {customer_count} customers to level 2.")


    return render(request, 'client/home/register.html')

def user_logout(request):
    logout(request)
    return render(request, 'client/home/index.html')
def forgotPassword(request):
    return render(request, 'client/home/forgot.html')