from rest_framework import serializers
from .models import User, Nominee, Company, InsurancePolicy, Customer, PolicyPurchase, Claim, Payment
from django.contrib.auth.hashers import make_password




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    


class CustomerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ('username', 'password', 'name_of_customer', 'age', 'gender', 'email', 'mobile')

    def create(self, validated_data):
        # print(validated_data)
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password = make_password(password)
        email = validated_data.get('email')
        # print(validated_data,username,password,email)
        user = User.objects.create(username=username, email=email, password=password, is_customer=True)
        customer = Customer.objects.create(user=user, **validated_data)
        # print(user,customer)
        return customer    




class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields ='__all__'

    

class CompanyRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ('name_of_company', 'password', 'headquarters', 'contact_number', 'company_address', 'email')

    def create(self, validated_data):
        name_of_company = validated_data.get('name_of_company')
        password = validated_data.pop('password')
        password=make_password(password)
       
        email = validated_data.get('email')
        user = User.objects.create_user(username=name_of_company, email=email, password=password, is_company=True)
        company = Company.objects.create(user=user, **validated_data)
        return company    


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=30)
    password=serializers.CharField(max_length=30)

    




class NomineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nominee
        fields = '__all__'


class InsurancePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'


class PolicyPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyPurchase
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
