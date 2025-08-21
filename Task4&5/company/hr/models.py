# Create your models here.
import uuid
from django.db import models

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # base salary in integer currency units (e.g., rupees). Null until set.
    base_salary = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', db_index=True)

    def __str__(self):
        return f"{self.name} ({self.department})"

    class Meta:
        indexes = [
            models.Index(fields=['department', 'base_salary']),
            models.Index(fields=['base_salary']),
        ]


class LeaveApplication(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_applications')
    month = models.CharField(max_length=20)   # e.g., "July"
    year = models.IntegerField()              # e.g., 2025
    leaves = models.IntegerField(default=0)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        indexes = [
            models.Index(fields=['employee', 'month', 'year']),
            models.Index(fields=['month', 'year']),
        ]

    def __str__(self):
        return f"Leaves: {self.employee} {self.month}-{self.year} = {self.leaves}"

