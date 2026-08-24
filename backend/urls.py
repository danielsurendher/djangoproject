from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('features/', views.features, name='features'),
    path('pricing/', views.pricing, name='pricing'),
    path('add_student/', views.add_student, name='add_student'),
    path('view_students/', views.view_students, name='view_students'),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('view-students/',views.view_students,name='view_students'),
    path('pricing/',views.pricing,name='pricing'),
    path('payment/',views.payment,name='payment'),
    path('payment-submit/',views.payment_submit,name='payment_submit'),

]