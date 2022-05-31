from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth import logout

from .forms import SignUpForm
from .services import authenticate_and_login


class LoginView(View):
    """Login user into account"""
    def get(self, request):
        """Return login form page"""
        return render(request, "accounts/login.html")

    def post(self, request):
        """Login user"""
        return authenticate_and_login(request)


class LogoutView(View):
    """Loguout user"""
    def get(self, request):
        logout(request)
        return redirect('login')


class SignUpView(CreateView):
    """Registration a new user"""
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/register.html'
