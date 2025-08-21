from rest_framework import serializers
from .models import Department, Employee, LeaveApplication

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.UUIDField()  # accept uuid in requests

    class Meta:
        model = Employee
        fields = ['id', 'name', 'base_salary', 'department']


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['id', 'employee', 'month', 'year', 'leaves']
