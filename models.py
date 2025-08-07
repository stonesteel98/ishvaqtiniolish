from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.check_in.strftime('%Y-%m-%d')}"