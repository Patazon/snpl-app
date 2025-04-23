from django.contrib import admin

from dashboard.models import (
    Branch,
    Client,
    Contract,
    ContractStatus,
    Payment,
    PaymentMode,
    Product,
    Salesteam,
)

# Register your models here.
# admin.site.register(AccountNumber)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(PaymentMode)
admin.site.register(Salesteam)
admin.site.register(Branch)
admin.site.register(ContractStatus)
