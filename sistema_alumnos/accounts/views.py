from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            
            try:
                subject = "Bienvenido/a"
                message = ""
                html_message = f"<h3>Hola {user.username}!</h3><p>Bienvenido/a al sistema.</p>"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email],
                          fail_silently=False, html_message=html_message)
            except Exception:
                pass
            
            login(request, user)
            messages.success(request, "Registro exitoso. Bienvenido/a.")
            return redirect("alumnos:dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("alumnos:dashboard")
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido {username}!")
                return redirect("alumnos:dashboard")
    else:
        form = AuthenticationForm()
    
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('accounts:login')

# AÑADE ESTA VISTA QUE FALTABA
@login_required
def logout_confirm(request):
    """Vista para confirmar cierre de sesión"""
    return render(request, 'accounts/logout_confirm.html')