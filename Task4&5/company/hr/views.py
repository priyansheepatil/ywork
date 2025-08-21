from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import F
from .models import Department, Employee, LeaveApplication
from .serializers import DepartmentSerializer, EmployeeSerializer, LeaveApplicationSerializer

# Dept & Employee basic viewsets (create/list ...)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @action(detail=True, methods=['get'])
    def high_earners(self, request, pk=None):
        """
        Returns employees whose base_salary is in top 3 unique base salaries for that department.
        """
        dept = self.get_object()
        # get unique base salaries descending
        unique_salaries = list(
            Employee.objects.filter(department=dept, base_salary__isnull=False)
            .values_list('base_salary', flat=True).distinct().order_by('-base_salary')[:3]
        )
        employees = Employee.objects.filter(department=dept, base_salary__in=unique_salaries)
        serializer = EmployeeSerializer(employees, many=True)
        return Response({'top_salaries': unique_salaries, 'employees': serializer.data})


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['post'])
    def set_base_salary(self, request, pk=None):
        """POST: {"base_salary": 50000}"""
        emp = self.get_object()
        base = request.data.get('base_salary')
        if base is None:
            return Response({"error": "base_salary is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            base = int(base)
        except ValueError:
            return Response({"error": "base_salary must be integer"}, status=status.HTTP_400_BAD_REQUEST)
        emp.base_salary = base
        emp.save()
        return Response(EmployeeSerializer(emp).data)

    @action(detail=True, methods=['post'])
    def payable_salary(self, request, pk=None):
        """
        POST with {"month":"July", "year":2025}
        Returns payable salary: base - leaves*(base/25).
        """
        emp = self.get_object()
        if emp.base_salary is None:
            return Response({"error": "Employee base_salary not set"}, status=status.HTTP_400_BAD_REQUEST)
        month = request.data.get('month')
        year = request.data.get('year')
        if not month or not year:
            return Response({"error":"month and year required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            year = int(year)
        except ValueError:
            return Response({"error":"year must be integer"}, status=status.HTTP_400_BAD_REQUEST)

        la = LeaveApplication.objects.filter(employee=emp, month=month, year=year).first()
        leaves = la.leaves if la else 0

        # use Decimal to avoid floating rounding issues
        base = Decimal(emp.base_salary)
        payable = (base - Decimal(leaves) * (base / Decimal(25))).quantize(Decimal('0.01'))

        return Response({
            'employee_id': emp.id,
            'base_salary': int(emp.base_salary),
            'month': month,
            'year': year,
            'leaves': leaves,
            'payable_salary': str(payable)
        })


@api_view(['POST'])
def increment_leave(request):
    """
    POST {"employee": 1, "month": "July", "year": 2025, "increment": 1}
    Creates or updates the LeaveApplication row and increases leaves by increment.
    """
    emp_id = request.data.get('employee')
    month = request.data.get('month')
    year = request.data.get('year')
    inc = int(request.data.get('increment', 1))
    if not emp_id or not month or year is None:
        return Response({"error":"employee, month, year required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        year = int(year)
    except ValueError:
        return Response({"error":"year must be integer"}, status=status.HTTP_400_BAD_REQUEST)

    emp = get_object_or_404(Employee, id=emp_id)
    obj, created = LeaveApplication.objects.get_or_create(employee=emp, month=month, year=year,
                                                         defaults={'leaves': 0})
    obj.leaves = obj.leaves + inc
    obj.save()
    return Response(LeaveApplicationSerializer(obj).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def department_high_earners_month(request, dept_pk):
    """
    GET /api/departments/<dept_pk>/high_earners_month/?month=July&year=2025
    Returns employees in department whose payable salary for that month is in the top 3 unique payable salaries.
    """
    month = request.query_params.get('month')
    year = request.query_params.get('year')
    if not month or year is None:
        return Response({"error":"month and year required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        year = int(year)
    except ValueError:
        return Response({"error":"year must be integer"}, status=status.HTTP_400_BAD_REQUEST)

    dept = get_object_or_404(Department, pk=dept_pk)
    employees = Employee.objects.filter(department=dept, base_salary__isnull=False)

    from decimal import Decimal
    emp_payable = []
    for e in employees:
        la = LeaveApplication.objects.filter(employee=e, month=month, year=year).first()
        leaves = la.leaves if la else 0
        base = Decimal(e.base_salary)
        payable = (base - Decimal(leaves) * (base / Decimal(25))).quantize(Decimal('0.01'))
        emp_payable.append((e, payable))

    # get unique payables sorted desc, pick top 3
    unique_payables = sorted({p for (_, p) in emp_payable}, reverse=True)[:3]
    result = []
    for e, p in emp_payable:
        if p in unique_payables:
            ser = EmployeeSerializer(e).data
            ser.update({'payable_salary': str(p)})
            result.append(ser)

    return Response({'top_payables': [str(x) for x in unique_payables], 'employees': result})

