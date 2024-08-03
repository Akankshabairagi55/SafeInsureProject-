from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Company, Nominee, InsurancePolicy, PolicyPurchase, Claim, Payment, User
from .serializers import CustomerSerializer, CustomerRegisterSerializer, CompanyRegisterSerializer, CompanySerializer, NomineeSerializer, InsurancePolicySerializer, PolicyPurchaseSerializer, ClaimSerializer, PaymentSerializer

# Customer Views
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only authenticated admin can list and create customers

class CustomerRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({'detail': 'Customer registered successfully', 'customer_id': customer.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access customer details

# Company Views
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only authenticated admin can list and create companies

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access company details

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
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
    permission_classes = [IsAuthenticated]  # Only authenticated users can list and create nominees

class NomineeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access nominee details

# InsurancePolicy Views
class InsurancePolicyListCreateView(generics.ListCreateAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list and create insurance policies

class InsurancePolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access insurance policy details

# PolicyPurchase Views
class PolicyPurchaseListCreateView(generics.ListCreateAPIView):
    queryset = PolicyPurchase.objects.all()
    serializer_class = PolicyPurchaseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list and create policy purchases

class PolicyPurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PolicyPurchase.objects.all()
    serializer_class = PolicyPurchaseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access policy purchase details

# Claim Views
class ClaimListCreateView(generics.ListCreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list and create claims

class ClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access claim details

# Payment Views
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can list and create payments

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access payment details
