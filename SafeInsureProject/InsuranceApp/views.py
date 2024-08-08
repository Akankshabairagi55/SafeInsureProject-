from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from .permissions import isCustomer,isCompany
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken ,BlacklistedToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied

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
    def get_object(self):
        user=super().get_object(self)
        if self.request.user.username!=user.username:
            PermissionDenied(detail='You do not have permission to access this user')

        return user   

    

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


#LogOut View:

class LogoutView(APIView):
    def post(self,request):
        try:
            token=OutstandingToken.objects.filter(user=request.user).latest('created_at')
            BlacklistedToken.objects.create(token=token)
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



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
    permission_classes = [IsAuthenticatedOrReadOnly]


    
    
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
    
