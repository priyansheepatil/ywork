from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DepartmentViewSet, EmployeeViewSet, increment_leave, department_high_earners_month

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('leaves/increment/', increment_leave, name='increment-leave'),
    path('departments/<uuid:dept_pk>/high_earners_month/', department_high_earners_month, name='dept-high-earners-month'),
]
