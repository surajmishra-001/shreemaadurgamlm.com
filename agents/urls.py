from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name="user"),
    path('tree', views.index, name="tree"),
    path('profile', views.profile, name="profile"),
    path('network', views.get_parent_data, name="network"),
    path('add-member', views.addMember, name="add-new-member"),
    path('business-plan', views.businessPlan, name="business-plan"),
    path('network/<str:user>', views.singleUserNetwork, name="single-user-network"),
    path('test', views.testLevel, name="test"),
    path('test/<int:level>', views.testLevel, name="test"),
    path('level/<int:level>', views.testLevel, name="test"),
    path('support', views.support, name="support"),
    path('income-history', views.incomeHistory, name="income-history"),
    path('income-history/<str:user>', views.incomeHistoryCalculate, name="income-history"),
    path('wallet', views.walllet, name="wallet"),
    path('update-password', views.updatePassword, name="update-password"),
    path('repurchase', views.repurchase, name="repurchase"),
    path('reward', views.reward, name="reward"),
    path('funds', views.repurchaseReward, name="funds"),
    path('repurchase-income', views.repurchaseIncome, name="repurchase-income"),
    path('get-user-detail/<str:user>', views.user_detail, name="get_user_detai"),
    path('get-sponsor-detail/<str:user>', views.sponsor_detail, name="get_sponsor_detai"),
    path('get-parent-detail/<str:user>', views.parent_detail, name="get_parent_detai"),




    # path('parent', views.get_parent_data, name="support"),
]