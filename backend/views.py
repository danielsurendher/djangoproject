from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from backend.models import student
from .form import UserForm
from backend.models import student, Payment
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

@login_required(login_url='')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='')
def features(request):
    return render(request, 'features.html')

@login_required(login_url='')
def pricing(request):
    return render(request, 'pricing.html')

@login_required(login_url='')
def add_student(request):
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()
            return redirect('add_student')  # Redirect to a success page after saving
    else:
        form = UserForm()
    
    return render(request, 'student.html', {'form': form})

@login_required(login_url='')
def view_students(request):

    search = request.GET.get('search', '').strip()

    students = student.objects.all()

    if search:
        students = students.filter(
            studentname__icontains=search
        )

    payment_data = []

    if search:

        for s in students:

            payments = Payment.objects.filter(
                student=s
            ).order_by('-payment_date')

            if payments.exists():

                # Course fee should NOT be added for every installment
                total_fee = payments.first().total_fee

                # Add all actual payments
                total_paid = sum(
                    payment.paid_amount
                    for payment in payments
                )

                # Calculate pending
                pending = total_fee - total_paid

            else:

                total_fee = 0
                total_paid = 0
                pending = 0

            payment_data.append({
                'student': s,
                'payments': payments,
                'total_fee': total_fee,
                'total_paid': total_paid,
                'pending': pending
            })

    return render(request, 'viewstudent.html', {
        'add_student': students,
        'search': search,
        'payment_data': payment_data
    })
@login_required(login_url='')
def edit_student(request, id):
    student_instance = student.objects.get(id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=student_instance)

        if form.is_valid():
            form.save()
            return redirect('view_students')

    else:
        form = UserForm(instance=student_instance)

    

    return render(request, 'student.html', {
        
        'form': form,  
        'edit_student': student_instance      
    })



@login_required(login_url='')
def delete_student(request, id):
    student_instance = student.objects.get(id=id)
    student_instance.delete()
    return redirect('view_students')  # Redirect to the view_students page after deletion



@login_required(login_url='')
def pricing(request):
    return render(request, 'pricing.html')


@login_required(login_url='')
def payment(request):

    course = request.GET.get('course')
    amount = request.GET.get('amount')

    students = student.objects.all().order_by('studentname')

    return render(request, 'payment.html', {
        'course': course,
        'amount': amount,
        'students': students
    })



@login_required(login_url='')
def payment_submit(request):

    if request.method == 'POST':

        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        total_fee = Decimal(request.POST.get('total_fee'))
        paid_amount = Decimal(request.POST.get('paid_amount'))
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')

        selected_student = get_object_or_404(
            student,
            id=student_id
        )

        # Existing payments for this student and course
        previous_payments = Payment.objects.filter(
            student=selected_student,
            course=course
        )

        previous_paid = sum(
            payment.paid_amount
            for payment in previous_payments
        )

        # Current pending amount
        pending_before_payment = total_fee - previous_paid

        # Prevent paying more than pending amount
        if paid_amount > pending_before_payment:

            return render(request, 'payment.html', {
                'course': course,
                'amount': total_fee,
                'students': student.objects.all(),
                'error':
                    f'Payment cannot exceed pending amount '
                    f'₹{pending_before_payment}'
            })

        # Save payment
        Payment.objects.create(
            student=selected_student,
            course=course,
            total_fee=total_fee,
            paid_amount=paid_amount,
            payment_method=payment_method,
            transaction_id=transaction_id
        )

        # Calculate new totals
        total_paid = previous_paid + paid_amount
        pending_amount = total_fee - total_paid

        return render(request, 'payment_success.html', {
            'student': selected_student,
            'course': course,
            'total_fee': total_fee,
            'paid_amount': paid_amount,
            'total_paid': total_paid,
            'pending_amount': pending_amount,
            'payment_method': payment_method
        })

    return redirect('pricing')