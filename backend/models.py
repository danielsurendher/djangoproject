from django.db import models


class student(models.Model):
    studentname = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    picture = models.ImageField(
        upload_to='images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.studentname


class Payment(models.Model):

    student = models.ForeignKey(
        student,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    course = models.CharField(max_length=100)

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.student.studentname} - {self.course}"