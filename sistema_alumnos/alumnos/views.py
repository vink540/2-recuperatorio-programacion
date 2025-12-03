from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno
from .forms import AlumnoForm
from django.http import HttpResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.conf import settings
import csv

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, "alumnos/dashboard.html", {"alumnos": alumnos})

@login_required
def crear_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            return redirect("alumnos:dashboard")
    else:
        form = AlumnoForm()
    return render(request, "alumnos/crear_alumno.html", {"form": form})

@login_required
def generar_pdf_enviar(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    # crear PDF en memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Ficha del alumno: {alumno.nombre} {alumno.apellido}")
    p.drawString(100, 780, f"DNI: {alumno.dni}")
    p.drawString(100, 760, f"Año: {alumno.anio}")
    p.drawString(100, 740, f"División: {alumno.division}")
    p.drawString(100, 780, f"Nota: {alumno.nota}")
    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"alumno_{alumno.id}.pdf"

    # intentar enviar por email
    try:
        email = EmailMessage(
            subject=f"Ficha de {alumno.nombre}",
            body="Adjunto PDF con la ficha del alumno.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],  # o email del docente si quisieras
        )
        email.attach(filename, buffer.getvalue(), "application/pdf")
        email.send(fail_silently=False)
        return render(request, "alumnos/pdf_result.html", {"ok": True, "mensaje": "Email enviado correctamente."})
    except Exception as e:
        # fallback: devolver el PDF para descargar
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=filename)
        return response

@login_required
def export_csv(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre', 'apellido', 'nota'])
    for a in alumnos:
        writer.writerow([a.nombre, a.apellido, str(a.nota)])
    return response

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        nombre_completo = alumno.nombre_completo
        alumno.delete()
        messages.success(request, f'Alumno {nombre_completo} eliminado exitosamente.')
        return redirect('alumnos:dashboard')
    
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            alumno_actualizado = form.save()
            messages.success(request, f'Alumno {alumno_actualizado.nombre_completo} actualizado exitosamente.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'alumnos/editar_alumno.html', {
        'form': form,
        'alumno': alumno
    })