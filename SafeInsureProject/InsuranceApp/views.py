from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from .permissions import isCustomer,isCompany

# Customer Views
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
   

class CustomerRegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({'detail': 'Customer registered successfully', 'customer_id': customer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[isCustomer]
    

# Company Views
class CompanyListCreateView(generics.ListCreateAPIView):
    permission_classes=[AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer
   

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes=[isCompany]
    

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user=User.objects.filter(username=username).first()
        # user = authenticate(username=username, password=password)

        
        if user is not None:
            if user.is_customer or user.is_company:
                refresh = RefreshToken.for_user(user)
                user_type = 'customer' if user.is_customer else 'company'
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_type': user_type
                })
            else:
                return Response({'detail': 'User type not recognized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Nominee Views
class NomineeListCreateView(generics.ListCreateAPIView):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
   
    

class NomineeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    permission_classes=[isCustomer]
    
# InsurancePolicy Views
class InsurancePolicyListCreateView(generics.ListCreateAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer


    
    
class InsurancePolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    
# PolicyPurchase Views
class PolicyPurchaseListCreateView(generics.ListCreateAPIView):
    queryset = PolicyPurchase.objects.all()
    serializer_class = PolicyPurchaseSerializer
   

class PolicyPurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PolicyPurchase.objects.all()
    serializer_class = PolicyPurchaseSerializer
   

# Claim Views
class ClaimListCreateView(generics.ListCreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    

class ClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    

# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
   

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
