from django.urls import path
from .views import (
    
    CustomerListCreateView, CustomerDetailView,
    CompanyListCreateView, CompanyDetailView,
    NomineeListCreateView, NomineeDetailView,
    InsurancePolicyListCreateView, InsurancePolicyDetailView,
    PolicyPurchaseListCreateView, PolicyPurchaseDetailView,
    ClaimListCreateView, ClaimDetailView,
    PaymentListCreateView, PaymentDetailView,LoginView,CustomerRegisterView
)

urlpatterns = [
    

    # Customer URLs
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Company URLs
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    #customer sign up
    path('signup/', CustomerRegisterView.as_view(), name='signup'),

    #login

     path('api/login/', LoginView.as_view(), name='login'),

    # Nominee URLs
    path('nominees/', NomineeListCreateView.as_view(), name='nominee-list-create'),
    path('nominees/<int:pk>/', NomineeDetailView.as_view(), name='nominee-detail'),

    # InsurancePolicy URLs
    path('policies/', InsurancePolicyListCreateView.as_view(), name='policy-list-create'),
    path('policies/<int:pk>/', InsurancePolicyDetailView.as_view(), name='policy-detail'),

    # PolicyPurchase URLs
    path('purchases/', PolicyPurchaseListCreateView.as_view(), name='purchase-list-create'),
    path('purchases/<int:pk>/', PolicyPurchaseDetailView.as_view(), name='purchase-detail'),

    # Claim URLs
    path('claims/', ClaimListCreateView.as_view(), name='claim-list-create'),
    path('claims/<int:pk>/', ClaimDetailView.as_view(), name='claim-detail'),

    # Payment URLs
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
