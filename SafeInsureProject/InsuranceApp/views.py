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
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

# Customer Views
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[isCompany]
    

    def get_queryset(self):
        company=Company.objects.get(user=self.request.user)


        return Customer.objects.filter(
            purchases__policy__company=company
        ).distinct()
   

class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes=[AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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

    

# Company Register  Views
class CompanyRegisterView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanyRegisterSerializer


# Company List Views
class CompanyListView(generics.ListAPIView):
    permission_classes=[isCustomer]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer



   

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes=[isCompany]

    def get_object(self):
        company=super().get_object(self)
        if self.request.user.username!=company.name_of_company:
            PermissionDenied(detail='You do not have permission to access this user')

        return company

class LoginView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class = LoginSerializer


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



    # Nominee create View
class NomineeCreateView(generics.CreateAPIView):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    permission_classes=[isCustomer]

    def post(self,request):
        customer_profile=Customer.objects.filter(user=request.user.id).first()
        request.data['customer']=customer_profile.id
        serializer=self.get_serializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Nominee Added Successfully'})    
        

class NomineesListView(generics.ListAPIView):
    serializer_class=NomineeSerializer
    permission_classes=[isCustomer]

    def get_queryset(self):
        #getting logged-in customer from checking it through the User model (one-to-one relation)

        customer=self.request.user.customer
        
        # Filter nominees that belong to the logged-in customer
        return Nominee.objects.filter(customer=customer)


   
    

class NomineeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nominee.objects.all()
    serializer_class = NomineeSerializer
    permission_classes=[isCustomer]

    def get_object(self):
        nominee=super().get_object()

        # Check if the nominee is associated with the currently logged-in customer
        if not nominee.customers.filter(user=self.request.user).exists():
            raise PermissionDenied(detail='You do not have permission to access this nominee.')

        return nominee  

    
    
# InsurancePolicy  List Views
class InsurancePolicyListView(generics.ListAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [AllowAny]
    filter_backends=[SearchFilter]
    search_fields=['types_of_insurance','policy_name']

#InsurancePolicy Create Views
class InsurancePolicyCreateView(generics.CreateAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [isCompany] 

    def perform_create(self, serializer):
        # Get the company associated with the logged-in user
        company = Company.objects.get(user=self.request.user)
        serializer.save(company=company)


class InsurancePolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsurancePolicy.objects.all()
    serializer_class = InsurancePolicySerializer
    permission_classes = [isCustomer | isCompany]

    def get_queryset(self):
        # If the user is a customer, return only the policies they have purchased
        if self.request.user.is_customer:
            return InsurancePolicy.objects.filter(purchased_policies__customer__user=self.request.user)
        # If the user is a company, return only the policies they created
        elif self.request.user.is_company:
            return InsurancePolicy.objects.filter(company__user=self.request.user)
        return InsurancePolicy.objects.none()  # Return empty queryset if neither

    def perform_update(self, serializer):
        # Ensure that only the company that created the policy can update it
        if self.request.user.is_company and self.get_object().company.user == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this policy.")

    def perform_destroy(self, instance):
        # Ensure that only the company that created the policy can delete it
        if self.request.user.is_company and instance.company.user == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this policy.")

    
class PolicyPurchaseListView(generics.ListAPIView):
    serializer_class = PolicyPurchaseSerializer
    filter_backends = [SearchFilter]
    permission_classes=[isCompany]
    search_fields = ['customer__nameOfCustomer', 'policy__policy_name']  # Update to search by related fields

    def get_queryset(self):
        user = self.request.user
        
        if user.is_company:
            # Return only PolicyPurchases associated with the company that the user is logged in
            company = Company.objects.get(user=user)
            return PolicyPurchase.objects.filter(policy__company=company)
        
        # Optionally, handle other cases if needed (e.g., if the user is a customer)
        return PolicyPurchase.objects.none()  # Return an empty queryset if the user is not a company

class PolicyPurchaseCreateView(generics.CreateAPIView):
    queryset = PolicyPurchase.objects.all()
    serializer_class = PolicyPurchaseSerializer
    permission_classes = [ isCustomer]  # Ensure only authenticated customers can access this view

    def perform_create(self, serializer):
        user = self.request.user
        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("User is not registered as a customer.")
        
        policy_id = self.request.data.get('policy')  # Assuming the policy ID is sent in the request data
        try:
            policy = InsurancePolicy.objects.get(id=policy_id)
        except InsurancePolicy.DoesNotExist:
            raise serializers.ValidationError("Policy does not exist.")

        # Create PolicyPurchase instance with the customer and selected policy
        serializer.save(customer=customer, policy=policy)
   



class PolicyPurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PolicyPurchaseSerializer
    permission_classes = [IsAuthenticated]
   

    def get_queryset(self):
        """
        Returns the queryset for the `Retrieve`, `Update`, and `Destroy` actions.
        """
        user = self.request.user
        if user.is_customer:
            # Customers can only view their own policy purchases
            return PolicyPurchase.objects.filter(customer__user=user)
        elif user.is_company:
            # Companies can view all policy purchases made for policies they issued
            return PolicyPurchase.objects.filter(policy__company__user=user)
        return PolicyPurchase.objects.none()  # Return an empty queryset if user is neither a customer nor a company

    def get_object(self):
        """
        Retrieves the object for the view, using the `get_queryset` method.
        """
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        
        # Additional check for permissions based on the request method
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if self.request.user.is_company:
                # Company can update/delete only its own policies
                if obj.policy.company.user != self.request.user:
                    self.permission_denied(self.request)
            elif self.request.user.is_customer:
                # Customers cannot update or delete their own policy purchases
                self.permission_denied(self.request)
        
        return obj

    def update(self, request, *args, **kwargs):
        """
        Handle PUT/PATCH requests to update the object. Ensure permissions are checked.
        """
        # Only companies can update policy purchases
        if request.user.is_customer:
            return Response({'detail': 'Customers cannot update policy purchases.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE requests to delete the object. Ensure permissions are checked.
        """
        # Only companies can delete policy purchases
        if request.user.is_customer:
            return Response({'detail': 'Customers cannot delete policy purchases.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

   
#claim list of customer (only company can see it)
class ClaimListView(generics.ListAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        """
        Returns the queryset for the `List` action based on user permissions.
        """
        user = self.request.user
        
        if user.is_company:
            # Filter claims based on policies issued by the company
            return Claim.objects.filter(policy_purchase__policy__company__user=user)
        
        # Return an empty queryset if the user is not a company
        return Claim.objects.none()
    


# Claim Create Views
class ClaimCreateView(generics.CreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [isCustomer]

    def perform_create(self, serializer):
        user = self.request.user
        
        # Check if the user is a customer
        if not user.is_customer:
            self.permission_denied(self.request, message="Only customers can create claims.")
        
        # Ensure the claim is associated with a policy purchase by the logged-in customer
        policy_purchase_id = self.request.data.get('policy_purchase')
        if not PolicyPurchase.objects.filter(id=policy_purchase_id, customer__user=user).exists():
            return Response({'detail': 'You can only claim policies you have purchased.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the claim with the policy purchase
        serializer.save()
    

class ClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This method returns the queryset for the `Retrieve`, `Update`, and `Destroy` actions.
        """
        user = self.request.user
        if user.is_customer:
            # Customer can only access their own claims
            return Claim.objects.filter(policy_purchase__customer__user=user)
        elif user.is_company:
            # Company can access claims related to the policies they have issued
            return Claim.objects.filter(policy_purchase__policy__company__user=user)
        return Claim.objects.none()  # Return an empty queryset if user is neither a customer nor a company

    def get_object(self):
        """
        This method retrieves the object for the view, using the `get_queryset` method.
        """
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        
        # Additional check for update and delete permissions
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if self.request.user.is_customer:
                # Customers cannot update or delete claims
                self.permission_denied(self.request)
            elif self.request.user.is_company:
                # Companies can update/delete only claims related to their own policies
                if obj.policy_purchase.policy.company.user != self.request.user:
                    self.permission_denied(self.request)
        
        return obj

    def update(self, request, *args, **kwargs):
        """
        Update method to handle PUT/PATCH requests. It checks if the user has permission to update the object.
        """
        self.check_object_permissions(request, self.get_object())
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy method to handle DELETE requests. It checks if the user has permission to delete the object.
        """
        self.check_object_permissions(request, self.get_object())
        return super().destroy(request, *args, **kwargs)
    

# Payment List Views
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, isCompany]

    def get_queryset(self):
        """
        Returns the queryset for the `List` action based on the logged-in company's policies.
        """
        user = self.request.user
        if user.is_company:
            return Payment.objects.filter(policy_purchase__policy__company__user=user)
        return Payment.objects.none()


# Payment  Create Views
class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, isCustomer]

    def perform_create(self, serializer):
        """
        This method is called when a valid `serializer` is passed to the view.
        """
        user = self.request.user
        
        # Check if the user is a customer
        if not user.is_customer:
            raise PermissionDenied("Only customers can create payments.")
        
        # Extract policy_purchase_id from the request data
        policy_purchase_id = self.request.data.get('policy_purchase')
        
        # Ensure the policy purchase exists and is associated with the logged-in customer
        try:
            policy_purchase = PolicyPurchase.objects.get(id=policy_purchase_id, customer__user=user)
        except PolicyPurchase.DoesNotExist:
            raise PermissionDenied("Invalid policy purchase or you do not have access to it.")
        
        # Save the payment
        serializer.save(policy_purchase=policy_purchase)
   

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Both customers and companies need to be authenticated

    def get_queryset(self):
        """
        This method returns the queryset for the `Retrieve`, `Update`, and `Destroy` actions.
        """
        user = self.request.user
        if user.is_customer:
            # Return only payments made by the logged-in customer
            return Payment.objects.filter(policy_purchase__customer__user=user)
        elif user.is_company:
            # Return payments related to policies issued by the logged-in company
            return Payment.objects.filter(policy_purchase__policy__company__user=user)
        return Payment.objects.none()  # Return an empty queryset if the user is neither a customer nor a company

    def get_object(self):
        """
        Retrieve the object for the view.
        """
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('pk'))

        # Additional checks for update and delete permissions
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if self.request.user.is_customer:
                # Customers cannot update or delete payments
                self.permission_denied(self.request)
            elif self.request.user.is_company:
                # Companies can update or delete payments only for their own policies
                if obj.policy_purchase.policy.company.user != self.request.user:
                    self.permission_denied(self.request)
        
        return obj

    def update(self, request, *args, **kwargs):
        """
        Update method to handle PUT/PATCH requests. It checks if the user has permission to update the object.
        """
        self.check_object_permissions(request, self.get_object())
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy method to handle DELETE requests. It checks if the user has permission to delete the object.
        """
        self.check_object_permissions(request, self.get_object())
        return super().destroy(request, *args, **kwargs)
    
