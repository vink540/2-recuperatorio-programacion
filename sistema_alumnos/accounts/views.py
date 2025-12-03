from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # enviar email de bienvenida (HTML sencillo)
            subject = "Bienvenido/a"
            message = ""
            html_message = f"<h3>Hola {user.username}!</h3><p>Bienvenido/a al sistema.</p>"
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email],
                          fail_silently=False, html_message=html_message)
            except Exception:
                # no rompemos el registro si falla el mail
                pass
            login(request, user)
            messages.success(request, "Registro exitoso. Bienvenido/a.")
            return redirect("alumnos:dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
