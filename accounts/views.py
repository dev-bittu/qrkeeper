from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already login. Logout first")
            return redirect("index")
        return render(request, "accounts/login.html")

    def post(self, request):
        email = request.POST.get("email", "")
        passwd = request.POST.get("password", "")

        if not (User.is_email_valid(email) and User.is_password_valid(passwd)):
            messages.warning(request, "Email or Password is not valid.")
            return redirect("accounts:login")

        user = authenticate(email=email, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in")
            return redirect("index")
        else:
            messages.warning(request, "Username or password is incorrect")
        return render(request, "accounts/login.html")

@method_decorator(login_required, name="dispatch")
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("accounts:login")

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect("index")
        return render(request, "accounts/register.html")
    
    def post(self, request):
        passwd1 = request.POST.get("password1", "")
        passwd2 = request.POST.get("password2", "")
        if passwd1 != passwd2:
            messages.warning(request, "Password not match")
            return redirect("accounts:register")

        email = request.POST.get("email", "")

        if not User.is_email_valid(email):
            messages.warning(request, "Email is not correct")
            return redirect("accounts:register")
        
        user = authenticate(email=email, password=passwd1)

        if user is None:
            user = User(email=email)
            user.set_password(passwd1)
            user.save()
            messages.success(request, "User created")
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "User already exists.")
            return redirect("accounts:register")
