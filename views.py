from django.shortcuts import render, redirect
from .models import Employee, Attendance
from django.utils import timezone
from django.contrib import messages

def check_in(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)

        # Hodim allaqachon bugun kirganmi — tekshiramiz
        today = timezone.now().date()
        already_checked = Attendance.objects.filter(
            employee=employee,
            check_in__date=today
        ).exists()

        if already_checked:
            messages.warning(request, f"{employee.name} bugun allaqachon ishga kirgan.")
        else:
            Attendance.objects.create(employee=employee)
            messages.success(request, f"{employee.name} ishga kirdi!")

        return redirect('check_in')

    return render(request, 'monitor/checkin.html', {'employees': employees})

def check_out(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)

        today = timezone.now().date()
        try:
            attendance = Attendance.objects.get(
                employee=employee,
                check_in__date=today,
                check_out__isnull=True
            )
            attendance.check_out = timezone.now()
            attendance.save()
            messages.success(request, f"{employee.name} ishni tugatdi!")
        except Attendance.DoesNotExist:
            messages.error(request, f"{employee.name} hali bugun ishga kirmagan yoki allaqachon chiqqan.")

        return redirect('check_out')

    return render(request, 'monitor/checkout.html', {'employees': employees})

def report(request):
    attendance_list = Attendance.objects.order_by('-check_in')[:50]  # oxirgi 50 yozuv
    return render(request, 'monitor/report.html', {'attendance_list': attendance_list})
