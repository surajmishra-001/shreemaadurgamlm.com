from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
from franchise.models import *
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date





def organize_agents(agents):
    agent_dict = {agent.id: {'agent': agent, 'children': []} for agent in agents}
    root_agents = []

    for agent_id, agent_info in agent_dict.items():
        sponsor_id = agent_info['agent'].sponsor_id
        if sponsor_id:
            agent_dict[sponsor_id]['children'].append(agent_info)
        else:
            root_agents.append(agent_info)

    return root_agents

def organize_data(agent):
    data = {
        'id': agent.id,
        'name': agent.name,
        'children': [],
    }

    # Recursively add children to the data
    for child in agent.referrals.all():
        child_data = organize_data(child)
        data['children'].append(child_data)

    return data



def index(request):
    agents = Accociate.objects.all()
    tree_data = organize_agents(agents)
    return render(request, 'template.html', {'tree_data': tree_data})

def userNetwork(request):
    # # Step 1: Get the current user
    # current_user = request.user

    # # Step 2: Retrieve the current user's Agent instance
    # try:
    #     agent = Agent.objects.get(user=current_user)
    # except Agent.DoesNotExist:
    #     # Handle the case where the current user doesn't have an associated Agent instance
    #     agent = None

    # # Step 3: Get the current user's network (downline)
    # downline = []
    # if agent:
    #     downline = agent.get_downline()

    # context = {
    #     'report': downline,
    # }
    data = Accociate.objects.get(user=request.user)
    level_1 = data.get_downline()[0:3]
    level_2 = data.get_downline()[3:9]
    level_2 = data.get_downline()[9:27]
    level_3 = data.get_downline()[27:81]
    level_4 = data.get_downline()[81:243]
    level_5 = data.get_downline()[243:729]
    level_6 = data.get_downline()[729:2187]
    level_7 = data.get_downline()[2187:6561]
    level_8 = data.get_downline()[6561:19683]
  
    
    context = {
        'data': data,
        'level_1': level_1,
        'level_2': level_2,
        'level_3': level_3,
        'level_4': level_4,
        'level_5': level_5,
        'level_6': level_6,
        'level_7': level_7,
        'level_8': level_8,
    }


    return render(request, 'client/user/user-network.html', context)

def organize_downline(agent):
    data = {
        'id': agent.id,
        'name': agent.name,
        'children': [],
    }

    # Recursively add children to the data
    for child in agent.referrals.all():
        child_data = organize_downline(child)
        data['children'].append(child_data)

    return data


def singleUserNetwork(request, user):
    # Step 1: Get the current user
    user = User.objects.get(username = user)

    # Step 2: Retrieve the current user's Agent instance
    try:
        agent = Agent.objects.get(user=user)
    except Agent.DoesNotExist:
        # Handle the case where the current user doesn't have an associated Agent instance
        agent = None

    # Step 3: Get the current user's network (downline)
    downline = []
    if agent:
        downline = agent.get_downline()
        data = agent.get_tree_data()
        


    context = {
        'report': downline,
    }

    return render(request, 'client/user/single-network.html', context)




def check_current_rank(data):
        # (12500000, "ambassador"),
        # (4200000, "royal ruby"),
        # (1450000, "ruby"),
        # (500000, "royal platinum"),
        # (165000, "platinum"),
        # (53000, "royal diamond"),
        # (17000, "diamond"),
        # (5500, "royal gold"),
        # (1800, "gold"),
        # (600, "silver"),
        # (190, "bronze"),
        # (65, "star"),

    rank = ''
    if data['level_15']  >= 12500000:
        rank = 'ambassador'
    elif data['level_14'] >= 4200000:
        rank = 'royal ruby'
    elif data['level_13'] >= 1450000:
        rank= 'ruby'
    elif data['level_12'] >= 500000:
        rank = 'royal platinum'
    elif data['level_11'] >= 165000:
        rank = 'platinum'
    elif data['level_10'] >= 53000:
        rank = 'royal diamond'
    elif data['level_9'] >=  17000:
        rank = 'diamond'
    elif data['level_8'] >= 5500:
        rank = 'royal gold'
    elif data['level_7'] >= 1800:
        rank = 'gold'
    elif data['level_6'] >=  600:
        rank = '600'
    elif data['level_5'] >= 190:
        rank = 'bronze'
    elif data['level_4'] >= 65:
        rank = 'star'         
    else:
        rank = 'No Rank'         



    return rank.capitalize()    

@login_required
def profile(request):
    today = date.today()
        
 
    
   
    is_redeem_visible = (today.day <= 5)
    user = request.user
    user_profile = Accociate.objects.get(user=user)
    total_downline_count = user_profile.get_total_downline_count() - 1

    current_profile = Accociate.objects.filter(parent=user_profile)

    data = {}
    d = 0
    for i in range(1, 16):
        d += print_level_income(current_profile, i).__len__()
        data[f'level_{i}'] = d
 

    # Check if the user already has a rank
    existing_rank = Reward.objects.filter(accociate=user_profile).first()

    if not existing_rank:
        # Define a list of rank conditions and their corresponding ranks
        rank_conditions = [
            (12500000, "ambassador"),
            (4200000, "royal ruby"),
            (1450000, "ruby"),
            (500000, "royal platinum"),
            (165000, "platinum"),
            (53000, "royal diamond"),
            (17000, "diamond"),
            (5500, "royal gold"),
            (1800, "gold"),
            (600, "silver"),
            (190, "bronze"),
            (65, "star"),
        ]

        # Initialize the default rank as None
        selected_rank = None

        # Check the conditions and select the highest rank that matches
        for condition, rank in rank_conditions:
            if total_downline_count >= condition:
                selected_rank = rank
                break  # Exit the loop when the first matching rank is found

        # Create a Reward object with the selected rank
        if selected_rank:
            new = Reward.objects.create(accociate=user_profile, rank=selected_rank)
            new.save()
        else:
            print("None of the conditions matched")
    if request.method =="POST":
        user_profile.name = request.POST['name']
        user_profile.email = request.POST['email']
        user_profile.phone = request.POST['phone']
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
        if 'aadhar_img' in request.FILES:
            user_profile.aadhar_img = request.FILES['aadhar_img']
        user_profile.pan = request.POST['pan']
        user_profile.account_number = request.POST['account_number']
        user_profile.bank_name = request.POST['bank_name']
        user_profile.branch_name = request.POST['branch_name']
        user_profile.bank_ifsc = request.POST['ifsc_code'] 
        dob = request.POST.get("dob", "");
        if dob:
            try:
                updated_dob = datetime.strptime(dob, "%Y-%m-%d")
                user_profile.dob = updated_dob
            except ValueError:
                messages.error(request, 'Invalid date format for Date of Birth.')
                return render(request, "client/user/profile.html")  # Replace with your template



        user_profile.save()

        messages.success(request, "Successfull Updated...")
        return redirect("profile")

    context = {"profile":user_profile, 'is_redeem_visible': is_redeem_visible, 'rank': check_current_rank(data)}
    return render(request, 'client/user/profile.html', context)


@login_required
def addMember(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        adhar = request.POST['adhar']
        pan = request.POST['pan']
        parent = request.POST['parent']
        leg = request.POST['leg']
        nominee = request.POST['nominee']
        dob = request.POST['dob']
        account_number = request.POST['account_number']
        sponsor = request.POST['sponsor']

        try:
            # Check sponsor_id
            user = User.objects.get(username=sponsor)
            sponsor = Accociate.objects.get(user=user)
        except Accociate.DoesNotExist:
            messages.error(request, 'Sponsor id not found')
            return redirect("profile")

        # Check if the email is already taken
        if email:
            email_exist = User.objects.filter(email=email).exists()
            if email_exist:
                messages.warning(request, "Email is already taken.")
                return redirect("profile")

        # Hash the password
        hashed_password = make_password(password)

        # Parse the date
        updated_dob = datetime.strptime(dob, "%Y-%m-%d")

        # Get the parent's Accociate object by searching for the parent's username
        try:
            parent_user = User.objects.get(username=parent)
            final_parent = Accociate.objects.get(user=parent_user)
        except User.DoesNotExist:
            messages.error(request, 'Parent user not found')
            return redirect("profile")
        except Accociate.DoesNotExist:
            messages.error(request, 'Parent Accociate not found')
            return redirect("profile")

        # Create a new User
        user = User.objects.create(username=username, password=hashed_password, email=email, first_name=name)
        user.save()

        # Create a new Accociate and link it to the User
        agent = Accociate.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            aadhar=adhar,
            pan=pan,
            dob=updated_dob,
            account_number=account_number,
            sponsor=sponsor,
            level=level,
            parent=final_parent,
            leg=leg,
            nominee=nominee
        )
        agent.save()

        messages.success(request, f"User {name} is added successfully.")
        return redirect("profile")


def businessPlan(request):
    return render(request, 'client/user/business-plan.html')


def test(request):
    data = Accociate.objects.get(user=request.user)
    
    context = {
        'data': data,
    }
    
    return render(request, 'client/user/test.html', context)


def testLevel(request, level):
    
    if level == 1:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[0:3]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 2:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[3:9]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 3:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[9:27]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 4:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[27:81]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 5:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[81:243]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 6:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[243:729]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 7:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[729:2187]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 8:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[2187:6561]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 9:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[6561:19683]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 10:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[19683:59049]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 11:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[59049:177147]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 12:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[177147:531441]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 13:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[531441:1594323]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 14:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[1594323:4782969]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level == 15:
        data = Accociate.objects.get(user=request.user)
        downline = data.get_downline()[4782969:14348907]
        context = {
            'report': downline,
        }
        return render(request, 'client/user/single-network.html', context) 
    
    if level < 15:
        return redirect('home')




def support(request):
    data = Support.objects.all()
    context = {"data":data}
    return render(request, "client/user/support.html", context)




def organize_downline_by_levels(root_user, max_levels=15):
    """
    Organize downline associates by their levels.
    Returns a dictionary where keys are levels and values are lists of associates at each level.
    """
    level_wise_downline = {}
    associate_queue = [(root_user, 0)]  # Start with the root user at level 1

    while associate_queue:
        associate, current_level = associate_queue.pop(0)

        if current_level not in level_wise_downline:
            level_wise_downline[current_level] = []

        level_wise_downline[current_level].append(associate)

        if current_level < max_levels:
            for referral in associate.referrals.all():
                # Check both sponsorship and parent relationships
                if referral.parent == associate:
                    associate_queue.append((referral, current_level + 1))

    return level_wise_downline





def level_data(request, level):
    # Get the current user
    current_user = Accociate.objects.get(user=request.user)

    # Define the maximum number of levels you want to organize
    max_levels = 15  # Change this to the desired number of levels

    # Organize the downline data for the current user
    level_wise_downline = organize_downline_by_levels(current_user, max_levels)

    # Create a context dictionary to pass the organized data to the template
    context = {
        "report": level_wise_downline,
        "level_key": level
    }
    return render(request, 'client/user/level_data.html', context)

@login_required
def user(request):
    return render(request, "client/user/user.html")

@login_required
def changePassword(request):
    user = User.objects.get(username__exact = request.user.username)
    password = request.POST['password']
    hashed_password = make_password(password)
    user.set_password(hashed_password)

    messages.success(request,"Password Changed Successfully..")

    return redirect('/user/profile')




# test 


def get_level_data(parent, max_depth=15, current_depth=1):
    level_data = []

    if current_depth <= max_depth:
        data = Accociate.objects.filter(parent=parent)
        level_data.append(data)

        for item in data:
            level_data.extend(get_level_data(item, max_depth, current_depth + 1))

    return level_data

def testParentdata(request, level=None):
    current_user = request.user.id
    initial_parent = Accociate.objects.get(user=current_user)  # Replace with the appropriate parent object
    all_level_data = get_level_data(initial_parent)

    if level is not None:
        try:
            level = int(level)
            if 1 <= level <= len(all_level_data):
                level_data = all_level_data[level - 1]
            else:
                level_data = []
        except ValueError:
            level_data = []
    else:
        level_data = all_level_data

    context = {"all_level_data": level_data, "level":level}

    return render(request, 'client/user/level_data.html', context)


def get_parent_data(request, level=None):
    current_user = request.user.id
    initial_parent = Accociate.objects.get(user=current_user)  # Replace with the appropriate parent object
    all_level_data = get_level_data(initial_parent)

    if level is not None:
        try:
            level = int(level)
            if 1 <= level <= len(all_level_data):
                level_data = all_level_data[level - 1]
            else:
                level_data = []
        except ValueError:
            level_data = []
    else:
        level_data = all_level_data

    context = {"all_level_data": level_data, "level":level}
   
    return render(request, 'client/user/level.html', context)


def print_level_data(data, target_level, current_level=1, max_levels=15):
    level_data = []

    if current_level == target_level:
        for item in data:
                level_data.append({
                    "name": item.name,
                    "phone": item.phone,
                    "parent": item.parent,
                    "sponsor": item.sponsor,
                    "leg": item.leg,
                    "status": item.is_active,
                })
        return level_data

    if current_level > max_levels:
        return []

    for item in data:
        child_data = Accociate.objects.filter(parent=item)
        level_data.extend(print_level_data(child_data, target_level, current_level + 1, max_levels))

    return level_data


def print_level_income(data, target_level, current_level=1, max_levels=15):
    level_data = []

    if current_level == target_level:
        for item in data:
            if item.is_active:
                level_data.append({
                    "name": item.name,
                    "phone": item.phone,
                    "parent": item.parent,
                    "sponsor": item.sponsor,
                    "leg": item.leg,
                    "status": item.is_active,
                })
        return level_data

    if current_level > max_levels:
        return []

    for item in data:
        child_data = Accociate.objects.filter(parent=item)
        level_data.extend(print_level_income(child_data, target_level, current_level + 1, max_levels))

    return level_data

def testLevel(request, level=None):
    current_user = Accociate.objects.get(user=request.user.id)
    level_1 = Accociate.objects.filter(parent=current_user)
    target_level = int(level) if level is not None else 1

    # Call the print_level_data function to retrieve the data for the specified level
    level_data = print_level_data(level_1, target_level)

    # Calculate the total income based on active members only
    active_member_count = sum(member['status'] for member in level_data)
    income_multiplier = {
        1: 50,
        2: 30,
        3: 15,
        4: 15,
        5: 10,
        6: 8,
        7: 5,
        8: 5,
        9: 5,
        10: 5,
        11: 4,
        12: 4,
        13: 2,
        14: 1,
        15: 1,
    }.get(target_level, 0)

    total_income = active_member_count * income_multiplier

    context = {"all_level_data": level_data, "level": target_level, "total_income": total_income}
    return render(request, 'client/user/test.html', context)


@login_required
def walllet(request, level=None):
    today = date.today()

   
    is_redeem_visible = today.day in (5, 20)
    if request.method == "POST":
        user_id = request.user.id 
        current_user = Accociate.objects.get(user=user_id)
        amount = request.POST['amount']
    
        redeem_request = Payment.objects.create(user=current_user, amount=amount)
        redeem_request.save()
        messages.success(request, "Redeem request succesfully submitted..")
        return redirect("/user/wallet")
    user = request.user.id
    current_user = Accociate.objects.get(user=user)
    level_1 = Accociate.objects.filter(parent=current_user)
    target_level = int(level) if level is not None else 1

    level_1_data = print_level_income(level_1, 1)
    level_2_data = print_level_income(level_1, 2)
    level_3_data = print_level_income(level_1, 3)
    level_4_data = print_level_income(level_1, 4)
    level_5_data = print_level_income(level_1, 5)
    level_6_data = print_level_income(level_1, 6)
    level_7_data = print_level_income(level_1, 7)
    level_8_data = print_level_income(level_1, 8)
    level_9_data = print_level_income(level_1, 9)
    level_10_data = print_level_income(level_1, 10)
    level_11_data = print_level_income(level_1, 11)
    level_12_data = print_level_income(level_1, 12)
    level_13_data = print_level_income(level_1, 13)
    level_14_data = print_level_income(level_1, 14)
    level_15_data = print_level_income(level_1, 15)


    payment_history = Payment.objects.filter(user=current_user)

    context = {
        "level_1":level_1_data,
        "level_2":level_2_data,
        "level_3":level_3_data,
        "level_4":level_4_data,
        "level_5":level_5_data,
        "level_6":level_6_data,
        "level_7":level_7_data,
        "level_8":level_8_data,
        "level_9":level_9_data,
        "level_10":level_10_data,
        "level_11":level_11_data,
        "level_12":level_12_data,
        "level_13":level_13_data,
        "level_14":level_14_data,
        "level_15":level_15_data,
        "payments":payment_history,
        'is_redeem_visible': is_redeem_visible
    }

    return render(request, "client/user/wallet.html", context)



@login_required
@permission_required('is_superuser')
def incomeHistory(request):
    member = Accociate.objects.all()
    context = {
        "members":member
    }
    return render(request, 'client/user/income-history.html', context)

@login_required
@permission_required('is_superuser')
def incomeHistoryCalculate(request, user, level=None):
    user = User.objects.get(username=user)
    current_user = Accociate.objects.get(user=user)
    name = current_user.name
    level_1 = Accociate.objects.filter(parent=current_user)
    target_level = int(level) if level is not None else 1

    level_1_data = print_level_income(level_1, 1)
    level_2_data = print_level_income(level_1, 2)
    level_3_data = print_level_income(level_1, 3)
    level_4_data = print_level_income(level_1, 4)
    level_5_data = print_level_income(level_1, 5)
    level_6_data = print_level_income(level_1, 6)
    level_7_data = print_level_income(level_1, 7)
    level_8_data = print_level_income(level_1, 8)
    level_9_data = print_level_income(level_1, 9)
    level_10_data = print_level_income(level_1, 10)
    level_11_data = print_level_income(level_1, 11)
    level_12_data = print_level_income(level_1, 12)
    level_13_data = print_level_income(level_1, 13)
    level_14_data = print_level_income(level_1, 14)
    level_15_data = print_level_income(level_1, 15)

    context = {
        "level_1":level_1_data,
        "level_2":level_2_data,
        "level_3":level_3_data,
        "level_4":level_4_data,
        "level_5":level_5_data,
        "level_6":level_6_data,
        "level_7":level_7_data,
        "level_8":level_8_data,
        "level_9":level_9_data,
        "level_10":level_10_data,
        "level_11":level_11_data,
        "level_12":level_12_data,
        "level_13":level_13_data,
        "level_14":level_14_data,
        "level_15":level_15_data,
        "name":name
    }

    return render(request, "client/user/wallet-check.html", context)


@login_required
def updatePassword(request):
    if request.method == "POST":
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            u = User.objects.get(username__exact=request.user.username)
            fpassword = make_password(password)
            u.set_password(password)
            u.save()
            messages.success(request, "Password Changed Succefully..")
            return redirect("/user/profile")
        else:
            messages.error(request, "Password does not matched..")
            return redirect("/user/profile")


@login_required
def repurchase(request):
    user = User.objects.get(username=request.user)
    accociate = Accociate.objects.get(user=user)
    history = RepurchaseSellHistory.objects.filter(user=accociate)
    context = {'history':history}
    return render(request, 'client/user/repurchase.html', context)


def reward(request):
    user = User.objects.get(username=request.user)
    accociate = Accociate.objects.get(user=user)
    history = Reward.objects.filter(accociate=accociate)
    context ={'history':history}
    return render(request, 'client/user/reward.html', context)

from django.shortcuts import get_object_or_404

def calculate_team_bv(user):
    repurchase_history = RepurchaseSellHistory.objects.filter(user=user)
    bv = sum(int(entry.product.BV) * int(entry.quantity) for entry in repurchase_history)

    associates = Accociate.objects.filter(sponsor=user)
    for associate in associates:
        bv += calculate_team_bv(associate)

    return bv


def repurchaseReward(request):
    user = get_object_or_404(User, username=request.user.username)
    accociate = get_object_or_404(Accociate, user=user)
    team = Accociate.objects.filter(sponsor=accociate)
    h = RepurchaseSellHistory.objects.filter(user=accociate)
    mybv = 0 

    for i in h:
        mybv += int(i.product.BV) * int(i.quantity)
    
    response_data = []

    team_bv_sum = 0 

    for teammate in team:
        repurchase_sell_history_entries = RepurchaseSellHistory.objects.filter(user=teammate)
        teammate_bv = calculate_team_bv(teammate)

        response_data.append({
            'teammate': teammate.name,
            'Total': teammate_bv,
        })

        team_bv_sum += teammate_bv

    total_sum = sum(entry['Total'] for entry in response_data)
    
    is_star = mybv >= 500 and any(entry['Total'] >= 3000 for entry in response_data) and team_bv_sum >= 4500
    print(is_star)

    # Check for 2-star ranking conditions
    is_gold = mybv >= 2000 and any(entry['Total'] >= 20000 for entry in response_data) and total_sum >= 30000
    is_diamond = mybv >= 5000 and any(entry['Total'] >= 120000 for entry in response_data) and total_sum >= 180000
    is_chairman = mybv >= 15000 and any(entry['Total'] >= 600000 for entry in response_data) and total_sum >= 900000

    return render(request, "client/user/repurchase-reward.html", context={
        "teams": response_data,
        "total_sum": total_sum,
        "is_star": is_star,
        "is_gold": is_gold,
        "is_diamond": is_diamond,
        "is_chairmain": is_chairman,
        "mybv":mybv

    })



# if a temaate have more 4500 bv count only 4500 bv and self bv more than 500 and another leg bv is 3000

def repurchase_level_data(data, target_level, current_level=1, max_levels=15):
    level_data = []

    if current_level == target_level:
        for item in data:
            level_data.append({
                "name": item.name,
                "user": item.user,
                "phone": item.phone,
                "parent": item.parent,
                "sponsor": item.sponsor,
                "leg": item.leg,
                "status": item.is_active,
            })
        return level_data

    if current_level > max_levels:
        return []

    for item in data:
        child_data = Accociate.objects.filter(sponsor=item)
        level_data.extend(repurchase_level_data(child_data, target_level, current_level + 1, max_levels))


    return level_data



from django.utils import timezone


def repurchase_income_calculate(request, _level, percent):
    user = get_object_or_404(User, username=request.user.username)
    accociate = get_object_or_404(Accociate, user=user)
    team = Accociate.objects.filter(sponsor=accociate)
    
    ''' '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    level = Accociate.objects.filter(sponsor=accociate)

    level_data = repurchase_level_data(level, _level)

    current_month = timezone.now().month

    # print(current_month)

    total_bv = 0
    for team in level_data:
        accociate = Accociate.objects.get(user=team['user'])
        bv = RepurchaseSellHistory.objects.filter(user=accociate)
        # print(bv)
        if bv:
            for bv_record in bv:
               if bv_record.created_at.month == current_month:
                    total = int(bv_record.quantity) * int(bv_record.product.BV)
                    total_bv += total


    return {"income":round(total_bv * percent/100), "accociate": len(level_data)}        
        



def repurchaseIncome(request):
    return render(request, "client/user/repurchase-income.html", context={
        "level_1":repurchase_income_calculate(request, _level=1, percent=25),
        "level_2":repurchase_income_calculate(request, _level=2, percent=18),
        "level_3":repurchase_income_calculate(request, _level=3, percent=12),
        "level_4":repurchase_income_calculate(request, _level=4, percent=8),
        "level_5":repurchase_income_calculate(request, _level=5, percent=6),
        "level_6":repurchase_income_calculate(request, _level=6, percent=4),
        "level_7":repurchase_income_calculate(request, _level=7, percent=3),
        "level_8":repurchase_income_calculate(request, _level=8, percent=2),
        "level_9":repurchase_income_calculate(request, _level=9, percent=2),
        "level_10":repurchase_income_calculate(request, _level=10, percent=1),
        "level_11":repurchase_income_calculate(request, _level=11, percent=1),
        "level_12":repurchase_income_calculate(request, _level=12, percent=1),
        "level_13":repurchase_income_calculate(request, _level=13, percent=1),
        "level_14":repurchase_income_calculate(request, _level=14, percent=.5),
        "level_15":repurchase_income_calculate(request, _level=15, percent=.5),
    })


''' 

Repurchase Plan : - agar user 1 level me hai aur uske 3 leg ki bv 135 ya usse jyada tab usko uski team ke bv me se 25% Milega

'''


from django.http import JsonResponse
from django.core.serializers import serialize

def user_detail(request, user):
    try:
        user_instance = User.objects.get(username=user)
        associate = Accociate.objects.get(user=user_instance)
        associate_instances = Accociate.objects.filter(parent=associate, is_active=True)

        # Extracting only the 'leg' field for JSON response
        leg_data = [{'leg': instance.leg, 'name':instance.name} for instance in associate_instances]

        # Using JsonResponse with safe=False to allow serialization of lists
        return JsonResponse(leg_data, safe=False)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except Accociate.DoesNotExist:
        return JsonResponse({'error': 'Associate not found'}, status=404)



def sponsor_detail(request, user):
    try:
        user_instance = User.objects.get(username=user)
        associate = Accociate.objects.get(user=user_instance, is_active=True)
        data = {
            'name': associate.name,
        }
        # Using JsonResponse with safe=False to allow serialization of lists
        return JsonResponse(data, safe=False)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except Accociate.DoesNotExist:
        return JsonResponse({'error': 'Associate not found'}, status=404)




def parent_detail(request, user):
    try:
        user_instance = User.objects.get(username=user)
        associate = Accociate.objects.get(user=user_instance, is_active=True)
        booked_legs = Accociate.objects.filter(parent=associate)

        legs = []

        for leg in booked_legs:
            legs.append(leg.leg)

        available_legs = set(['left', 'right', 'center']) - set(legs)



        data = {
            'name': associate.name,
            'legs': list(available_legs)
        }
        # Using JsonResponse with safe=False to allow serialization of lists
        return JsonResponse(data, safe=False)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except Accociate.DoesNotExist:
        return JsonResponse({'error': 'Associate not found'}, status=404)


