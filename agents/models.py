from django.db import models
from django.contrib.auth.models import User
from collections import deque
from collections import defaultdict


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, blank=True, null=True)
    profile_picture = models.FileField(upload_to="profile/", null=True, blank=True)
    aadhar = models.CharField(max_length=50, null=True, blank=True)
    pan = models.CharField(max_length=150, null=True, blank=True)
    account_number = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sponsor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    left_leg = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='left_referral')
    right_leg = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='right_referral')
    center_leg = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='center_referral')
   


    def __str__(self):
        return self.name


    def is_root_agent(self):
        """Check if the agent is the root agent (has no sponsor)."""
        return self.sponsor is None

    def has_left_leg(self):
        """Check if the agent has a left leg."""
        return self.left_leg is not None

    def has_right_leg(self):
        """Check if the agent has a right leg."""
        return self.right_leg is not None

    def has_center_leg(self):
        """Check if the agent has a center leg."""
        return self.center_leg is not None

    def can_add_to_left_leg(self):
        """Check if the agent can be added to the left leg."""
        return not self.is_root_agent() and not self.has_left_leg()

    def can_add_to_right_leg(self):
        """Check if the agent can be added to the right leg."""
        return not self.is_root_agent() and not self.has_right_leg()

    def can_add_to_center_leg(self):
        """Check if the agent can be added to the center leg."""
        return not self.is_root_agent() and not self.has_center_leg()

    def add_to_left_leg(self, agent):
        """Add an agent to the left leg."""
        if self.can_add_to_left_leg():
            self.left_leg = agent
            self.save()

    def add_to_right_leg(self, agent):
        """Add an agent to the right leg."""
        if self.can_add_to_right_leg():
            self.right_leg = agent
            self.save()

    def add_to_center_leg(self, agent):
        """Add an agent to the center leg."""
        if self.can_add_to_center_leg():
            self.center_leg = agent
            self.save()

    def get_downline(self):
        """Get all downline agents recursively."""
        downline = [self]
        for child in self.referrals.all():
            downline.extend(child.get_downline())
        return downline

    def get_level(self):
        """Calculate the agent's level based on the number of downline agents."""
        return len(self.get_downline()) - (3)  # Subtract 1 to exclude the agent

    def is_balanced(self):
        """Check if the agent's left and right legs are balanced."""
        left_leg_count = self.left_referral.count()
        right_leg_count = self.right_referral.count()
        return abs(left_leg_count - right_leg_count) <= 1

    def is_eligible_for_commission(self):
        """
        Check if the agent is eligible for commission (meets the criteria, e.g., balanced legs).
        You can customize this function based on your MLM plan rules.
        """
        return self.is_balanced() and self.get_level() >= 2  # Example criteria

    def calculate_commission(self):
        """Calculate commission for the agent based on your MLM plan rules."""
        if self.is_eligible_for_commission():
            # Implement your commission calculation logic here
            return 100  # Example commission amount
        return 0  # No commission

    def get_total_downline_count(self):
        """Get the total number of downline agents."""
        return len(self.get_downline())

    def get_total_left_leg_count(self):
        """Get the count of agents in the left leg."""
        return self.left_referral.count()

    def get_total_right_leg_count(self):
        """Get the count of agents in the right leg."""
        return self.right_referral.count()

    def get_total_center_leg_count(self):
        """Get the count of agents in the center leg."""
        return self.center_referral.count()




    def get_tree_data(self, level=0, leg=None, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            # Avoid revisiting agents to prevent infinite recursion
            return None

        visited.add(self)

        data = {
            'id': self.id,
            'name': self.name,
            'level': level,
            'children': [],
        }

        if leg == "left":
            children = [self.left_leg]
        elif leg == "center":
            children = [self.center_leg]
        elif leg == "right":
            children = [self.right_leg]
        else:
            children = [self.left_leg, self.center_leg, self.right_leg]

        for child in children:
            if child:
                child_data = child.get_tree_data(level + 1, leg, visited)
                if child_data:
                    data['children'].append(child_data)

        return data


legs = (
        ('left', 'left'),
        ('center', 'center'),
        ('right', 'right'),
    )
level = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
    )

class Accociate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, blank=True, null=True)
    profile_picture = models.FileField(upload_to="profile/", null=True, blank=True)
    aadhar = models.CharField(max_length=50, null=True, blank=True)
    aadhar_img = models.FileField(upload_to="aadhar/", null=True, blank=True)
    pan = models.CharField(max_length=150, null=True, blank=True)
    nominee = models.CharField(max_length=150, default="Nominee Name")
    account_number = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, default="Enter your bank Name..")
    bank_ifsc = models.CharField(max_length=150, default="")
    branch_name = models.CharField(max_length=200, default="Branch Name..")
    dob = models.DateField()
    address = models.TextField(default="Enter Your Address...")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    sponsor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    level = models.CharField(max_length=150, choices=level, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='pareint')
    leg = models.CharField(max_length=200, choices=legs, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    
    def is_root_agent(self):
        """Check if the agent is the root agent (has no sponsor)."""
        return self.sponsor is None

    def has_left_leg(self):
        """Check if the agent has a left leg."""
        return self.leg == 'left'

    def has_center_leg(self):
        """Check if the agent has a center leg."""
        return self.leg == 'center'

    def has_right_leg(self):
        """Check if the agent has a right leg."""
        return self.leg == 'right'

    def can_add_to_left_leg(self):
        """Check if the agent can be added to the left leg."""
        return not self.is_root_agent() and not self.has_left_leg()

    def can_add_to_center_leg(self):
        """Check if the agent can be added to the center leg."""
        return not self.is_root_agent() and not self.has_center_leg()

    def can_add_to_right_leg(self):
        """Check if the agent can be added to the right leg."""
        return not self.is_root_agent() and not self.has_right_leg()

    def add_to_left_leg(self, agent):
        """Add an agent to the left leg."""
        if self.can_add_to_left_leg():
            agent.leg = 'left'
            agent.save()

    def add_to_center_leg(self, agent):
        """Add an agent to the center leg."""
        if self.can_add_to_center_leg():
            agent.leg = 'center'
            agent.save()

    def add_to_right_leg(self, agent):
        """Add an agent to the right leg."""
        if self.can_add_to_right_leg():
            agent.leg = 'right'
            agent.save()

    def get_downline(self):
        """Get all downline agents recursively."""
        downline = [self]
        for referral in self.referrals.all():
            downline.extend(referral.get_downline())
        return downline
    
    def leve_1_downline(self):
        downline = [self]
        for referral in self.referrals.filter(level=1):
            downline.extend(referral.level_1_downline())
        return downline
    
    def organize_downline_by_levels(root_user, max_levels=15):
        """
        Organize downline associates by levels.
        
        Args:
            root_user (Accociate): The root user (level 0).
            max_levels (int): The maximum number of levels to organize.
        
        Returns:
            dict: A dictionary where keys are levels and values are lists of associates at each level.
        """
        level_wise_downline = defaultdict(list)
        downline = root_user.get_downline()
        
        for level in range(max_levels):
            level_associates = downline[:3 ** level]  # Calculate the number of associates at this level
            level_wise_downline[level + 1] = level_associates
            
            # Prepare downline for the next level
            downline = downline[3 ** level:]
        
        return dict(level_wise_downline)    

    def get_level(self):
        """Calculate the agent's level based on the number of downline agents."""
        return len(self.get_downline()) - 1  # Subtract 1 to exclude the agent itself

    def is_balanced(self):
        """Check if the agent's left and right legs are balanced."""
        left_leg_count = Accociate.objects.filter(sponsor=self, leg='left').count()
        right_leg_count = Accociate.objects.filter(sponsor=self, leg='right').count()
        return abs(left_leg_count - right_leg_count) <= 1

    def is_eligible_for_commission(self):
        """
        Check if the agent is eligible for commission (meets the criteria, e.g., balanced legs).
        You can customize this function based on your MLM plan rules.
        """
        return self.is_balanced() and self.get_level() >= 2  # Example criteria

    def calculate_commission(self):
        """Calculate commission for the agent based on your MLM plan rules."""
        if self.is_eligible_for_commission():
            # Implement your commission calculation logic here
            return 100  # Example commission amount
        return 0  # No commission

    def get_total_downline_count(self):
        """Get the total number of downline agents."""
        return len(self.get_downline())

    def get_level_wise_downline_count(self, level):
        """
        Get the count of downline associates for a specific level.
        """
        downline = self.get_downline()
        level_count = 0

        for associate in downline:
            associate_level = associate.get_level()
            if associate_level == level:
                level_count += 1

        return level_count



    def get_income(self):
        """
        Calculate income for the agent based on their level and total downline at that level.
        """
        level = self.get_level()
        total_downline = self.get_total_downline_count()

        # Define a dictionary to store prices for each level
        level_prices = {
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
            # Add more levels and prices as needed
        }

        if level in level_prices:
            return level_prices[level] * total_downline
        else:
            return 0

    def get_downline_count_by_level(self, level):
        """
        Calculate the number of downline associates for a specific level.
        Level 1: 3 associates, Level 2: 9 associates, Level 3: 27 associates, and so on.
        """
        if level < 1:
            return 0  # No downline for levels less than 1

        # Calculate the downline count based on the pattern 3^level
        return 3 ** (level - 1)

    def max_members_in_level(self, level):
        """
        Calculate the maximum number of members in a specific level.
        Level 1: 3 members, Level 2: 9 members, Level 3: 27 members, and so on.
        """
        if level < 1:
            return 0

    def get_parent_count_in_downline(self):
        """
        Get the count of parents (unique) in the downline.
        """
        downline = self.get_downline()
        parent_set = set()  # Use a set to store unique parents

        for associate in downline:
            if associate.parent:
                parent_set.add(associate.parent)

        return len(parent_set)
    

    def get_level_downline(self, level):
        """
        Get the 1st level downline (direct referrals) of the current user.
        """
        return Accociate.objects.filter(sponsor=self, level=level)    
    

    def get_parent_data_in_downline(self):
        """
        Get data of one parent in the downline.
        """
        downline = self.get_downline()

        for associate in downline:
            if associate.parent:
                parent_data = associate.parent  # Get the parent data
                # You can access parent_data and retrieve any fields you need
                return parent_data

        return None  # Re


    def __str__(self):
        return self.name



class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    
status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Done', 'Done'),
        ('Cancel', 'Cancel'),
    )
class Payment(models.Model):
    user  = models.ForeignKey(Accociate, on_delete=models.CASCADE)    
    amount = models.IntegerField()
    status = models.CharField(max_length=150, choices=status, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

rank = (
        ('ambassdor', 'ambassdor'),
        ('royal ruby', 'royal ruby'),
        ('ruby', 'ruby'),
        ('royal platinum', 'royal platinum'),
        ('platinum', 'platinum'),
        ('royal diamond', 'royal diamond'),
        ('diamond', 'diamond'),
        ('royal gold', 'royal gold'),
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('star', 'star'),
    )
class Reward(models.Model):
    id = models.AutoField(primary_key=True)    
    accociate = models.ForeignKey(Accociate, on_delete=models.CASCADE)
    rank = models.CharField(choices=rank, max_length=250)
    achiving_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.accociate)
        
        
    