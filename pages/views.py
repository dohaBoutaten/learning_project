from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'pages/home.html')
def login_view(request):
    return render(request, 'pages/login.html')

def register_view(request):
    return render(request, 'pages/register.html')

def dashboard_student(request):
    return render(request, 'pages/dashboard/dashboard_student.html')
def mes_cours(request):
    return render(request, 'pages/dashboard/mes_cours.html') 
def calendrier(request):
    return render(request, 'pages/dashboard/calendrier.html')
def progression(request):
    return render(request, 'pages/dashboard/progression.html')
def communaute(request):
    return render(request, 'pages/dashboard/communaute.html')
def certifications(request):
    return render(request, 'pages/dashboard/certifications.html')
def parametres(request):
    return render(request, 'pages/dashboard/parametres.html')


# ============================================
# VUES ADMINISTRATEUR
# ============================================

def admin_courses(request):
    return render(request, 'administrateur/admin_courses.html')

def admin_users(request):
    return render(request, 'administrateur/admin_users.html')

def admin_dashboard(request):
    return render(request, 'administrateur/admin_dashboard.html')


# ============================================
# VUES UTILISATEUR
# ============================================
def dashboard(request):
    return render(request, 'utilisateurs/dashboard.html')

def courses_available(request):
    return render(request, 'utilisateurs/courses_available.html')

def profil(request):
    return render(request, 'utilisateurs/profile.html')

def cours(request):
    return render(request, 'utilisateurs/cours.html')

def historique(request):
    return render(request, 'utilisateurs/historique.html')