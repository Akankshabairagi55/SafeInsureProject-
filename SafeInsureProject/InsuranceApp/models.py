from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)


class Nominee(models.Model):
    name_of_nominee = models.CharField(max_length=100)  # Name of the nominee
    relation=models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)  # Age of the nominee
    mobile = models.CharField(max_length=15, blank=True, null=True)  # Mobile number of the nominee

    def __str__(self):
        return self.name_of_nominee  # String representation of the nominee object    


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_of_company = models.CharField(max_length=100)  # Name of the company
    headquarters = models.CharField(max_length=200, blank=True, null=True)  # Location of the company's headquarters
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Company's contact number
    company_address = models.TextField(blank=True, null=True)  # Full address of the company
    email = models.EmailField(unique=True, blank=True, null=True)  # Unique email for the company

    def __str__(self):
        return self.name_of_company  # String representation of the company object


class InsurancePolicy(models.Model):
    TYPES_OF_INSURANCE = [
        ('health', 'Health Insurance'),
        ('car', 'Car Insurance'),
        ('life', 'Life Insurance'),
        ('home', 'Home Insurance'),
        ('term', 'Term Insurance'),
    ]

    types_of_insurance = models.CharField(max_length=50, choices=TYPES_OF_INSURANCE)  # Type of insurance
    policy_name = models.CharField(max_length=100)  # Name of the policy
    description = models.TextField(blank=True, null=True)  # Description of the policy
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Premium amount for the policy
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Coverage amount provided by the policy
    min_age = models.IntegerField(blank=True, null=True)  # Minimum eligible age for the policy
    max_age = models.IntegerField(blank=True, null=True)  # Maximum eligible age for the policy
    maturity_period = models.CharField(max_length=50, blank=True, null=True)  # Maturity period of the policy (e.g., "10 years")
    waiting_period = models.CharField(max_length=50, blank=True, null=True)  # Waiting period for policies like health insurance
    expiry_period = models.DateTimeField(blank=True, null=True)  # Expiry date for the policy
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='insurance_policies')  # Reference to the company offering the policy
    

    def __str__(self):
        return self.policy_name  # String representation of the policy object


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_of_customer = models.CharField(max_length=200)  # Name of the customer
    age = models.IntegerField(blank=True, null=True)  # Age of the customer
    
    gender = models.CharField(max_length=10, blank=True, null=True,choices=[('male','Male'),('female','Female'),('other','Other')])  # Gender of the customer
    email = models.EmailField(unique=True, blank=True, null=True)  # Unique email for the customer
    mobile = models.CharField(max_length=15, blank=True, null=True)  # Customer's mobile number
    nominee = models.ForeignKey(Nominee, on_delete=models.CASCADE, related_name='customers', blank=True, null=True)  # Nominee of the customer
    policies = models.ManyToManyField(InsurancePolicy, through='PolicyPurchase')  # Policies purchased by the customer

    def __str__(self):
        return self.name_of_customer  # String representation of the customer object


# PolicyPurchase model to track purchased policies
class PolicyPurchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='purchases')
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='purchased_policies')
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)  # Expiry date for the purchased policy
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('expired', 'Expired')], default='active')
    policy_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nominee_of_policy = models.ForeignKey(Nominee, on_delete=models.CASCADE, related_name='nominee_detail',null=True)

    def __str__(self):
        return f"{self.customer.name_of_customer} - {self.policy.policy_name}"


# Claim model to manage insurance claims
class Claim(models.Model):
    policy_purchase = models.ForeignKey(PolicyPurchase, on_delete=models.CASCADE, related_name='claims')
    description = models.TextField()
    claim_date = models.DateTimeField(auto_now_add=True)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Claim for {self.policy_purchase.policy.policy_name} by {self.policy_purchase.customer.name_of_customer}"


# Payment model to handle payment details
class Payment(models.Model):
    policy_purchase = models.ForeignKey(PolicyPurchase, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer')])

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.policy_purchase.policy.policy_name}"
