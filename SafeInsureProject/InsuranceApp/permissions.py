from rest_framework.permissions  import BasePermission


class isCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer==True
    

class isCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_company==True    