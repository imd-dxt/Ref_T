from rest_framework import viewsets
from .models import employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = employee.objects.all()
        name = self.request.query_params.get('name')
        userID = self.request.query_params.get('userID')
        organizationID = self.request.query_params.get('organizationID')
        role = self.request.query_params.get('role')
        if name is not None:
            queryset = queryset.filter(name=name)
        if userID is not None:
            queryset = queryset.filter(userID=userID)
        if organizationID is not None:
            queryset = queryset.filter(organizationID=organizationID)
        if role is not None:
            queryset = queryset.filter(role=role)
        return queryset

