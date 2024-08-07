from django.contrib import admin
from .models import User, Nominee, Company, InsurancePolicy, Customer, PolicyPurchase, Claim, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_company', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_customer', 'is_company', 'is_staff', 'is_active')

@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('name_of_nominee', 'relation', 'age', 'mobile')
    search_fields = ('name_of_nominee', 'mobile')
    list_filter = ('relation', 'age')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name_of_company', 'headquarters', 'contact_number', 'email')
    search_fields = ('name_of_company', 'email')
    list_filter = ('headquarters',)

@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'types_of_insurance', 'premium_amount', 'coverage_amount', 'company')
    search_fields = ('policy_name',)
    list_filter = ('types_of_insurance', 'company')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name_of_customer', 'age', 'gender', 'email', 'mobile')
    search_fields = ('name_of_customer', 'email', 'mobile')
    list_filter = ('gender', 'age')

@admin.register(PolicyPurchase)
class PolicyPurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'policy', 'purchase_date', 'expiry_date', 'status', 'policy_amount', 'nominee_of_policy')
    search_fields = ('customer__name_of_customer', 'policy__policy_name')
    list_filter = ('status', 'purchase_date', 'expiry_date')

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('policy_purchase', 'claim_date', 'claim_amount', 'claim_status')
    search_fields = ('policy_purchase__customer__name_of_customer', 'policy_purchase__policy__policy_name')
    list_filter = ('claim_status', 'claim_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('policy_purchase', 'payment_date', 'amount_paid', 'payment_method')
    search_fields = ('policy_purchase__customer__name_of_customer', 'policy_purchase__policy__policy_name')
    list_filter = ('payment_method', 'payment_date')
