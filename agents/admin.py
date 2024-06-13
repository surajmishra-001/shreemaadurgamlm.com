from django.contrib import admin
from . models import *
from import_export import resources
from import_export.admin import ExportActionMixin



class dataResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = ('user__name', 'amount', 'user__account_number', 'user__bank_ifsc')

# Register your models here.
class agentAdmin(admin.ModelAdmin):
    list_display = ["name", "left_leg", "right_leg", "center_leg", "sponsor" "status"]
    



class accociateAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "leg", "sponsor", "is_active"]
    search_fields = ["name", "phone"]
    list_filter = ["sponsor", "parent", "is_active"]


class paymentAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["user", "amount",  "status", "created_at",]
    list_filter = ['status', 'created_at', 'user']
    resource_classes = [dataResource]


admin.site.register(Accociate, accociateAdmin)
admin.site.register(Support)
admin.site.register(Reward)
admin.site.register(Payment, paymentAdmin)