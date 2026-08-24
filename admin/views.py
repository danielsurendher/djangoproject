from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('backend/add_student/')  # Redirect to the home page if the user is already logged in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('backend/home/')  # Redirect to the home page after successful login
   
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,  
            password=password
        )

        user.save()

        return redirect("login")

    return render(request, "signup.html")