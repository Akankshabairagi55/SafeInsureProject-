from django.contrib import admin

from .models import User, Nominee, Company, InsurancePolicy, Customer, PolicyPurchase, Claim, Payment


admin.site.register(User)
admin.site.register(Nominee)
admin.site.register(Company)
admin.site.register(InsurancePolicy)
admin.site.register(Customer)
admin.site.register(PolicyPurchase)
admin.site.register(Claim)
admin.site.register(Payment)


