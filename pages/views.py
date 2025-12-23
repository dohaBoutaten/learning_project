from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import  get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
# =====================
# PAGES PUBLIQUES
# =====================
def home(request):
    return render(request, 'pages/home.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'ADMIN':
                return redirect('administrateur_dashboard')
            else:
                return redirect('dashboard_student')

        messages.error(request, "Email ou mot de passe incorrect")

    return render(request, 'pages/login.html')


def register_view(request):
    if request.method == 'POST':
        prenom = request.POST.get('first_name')
        nom = request.POST.get('last_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 1️⃣ Vérification mots de passe
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect('register')

        # 2️⃣ Vérification email existant
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé")
            return redirect('register')

        # 3️⃣ Création utilisateur
        User.objects.create_user(
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            telephone=telephone

        )

        messages.success(request, "Compte créé avec succès. Connectez-vous.")
        return redirect('login')

    return render(request, 'pages/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# =====================
# DASHBOARD ÉTUDIANT
# =====================
@login_required
def dashboard_student(request):
    if request.user.role != 'ETUDIANT':
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'pages/dashboard/dashboard_student.html')


@login_required
def mes_cours(request):
    return render(request, 'pages/dashboard/mes_cours.html')


@login_required
def calendrier(request):
    return render(request, 'pages/dashboard/calendrier.html')


@login_required
def progression(request):
    return render(request, 'pages/dashboard/progression.html')


@login_required
def communaute(request):
    return render(request, 'pages/dashboard/communaute.html')


@login_required
def certifications(request):
    return render(request, 'pages/dashboard/certifications.html')


@login_required
def parametres(request):
    return render(request, 'pages/dashboard/parametres.html')


# =====================
# ADMINISTRATEUR
# =====================
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'administrateur/admin_dashboard.html')


@login_required
def admin_courses(request):
    return render(request, 'administrateur/admin_courses.html')


@login_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'administrateur/admin_users.html', {
        'users': users
    })



def add_user(request):
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        statut = request.POST.get('statut')
        telephone = request.POST.get('telephone')

        # Vérifications
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect('administrateur_users')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email existe déjà")
            return redirect('administrateur_users')

        user = User.objects.create(
            prenom=prenom,
            nom=nom,
            email=email,
            telephone=telephone,
            role='ADMIN' if role == 'admin' else 'ETUDIANT',
            is_active=True if statut == 'active' else False,
            password=make_password(password)
        )

        messages.success(request, "Utilisateur ajouté avec succès")
        return redirect('administrateur_users')


User = get_user_model()
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")

        user = get_object_or_404(User, id=user_id)

        user.prenom = request.POST.get("prenom")
        user.nom = request.POST.get("nom")
        user.email = request.POST.get("email")
        user.telephone = request.POST.get("telephone")

        # Rôle
        role = request.POST.get("role")
        user.role = "ADMIN" if role == "admin" else "STUDENT"

        # Statut
        statut = request.POST.get("statut")
        user.is_active = True if statut == "active" else False

        user.save()

        return redirect("administrateur_users")



def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        user.delete()

        messages.success(request, "Utilisateur supprimé avec succès 🗑️")

    return redirect("administrateur_users")

    

def administrateur_users(request):
    search = request.GET.get("search", "")
    role = request.GET.get("role", "")
    status = request.GET.get("status", "")

    users = User.objects.all().order_by("-date_joined")

    # Recherche
    if search:
        users = users.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(email__icontains=search) |
            Q(telephone__icontains=search)
        )

    # Filtre rôle
    if role:
        users = users.filter(role=role.upper())

    # Filtre statut
    if status == "active":
        users = users.filter(is_active=True)
    elif status == "inactive":
        users = users.filter(is_active=False)

    # Pagination
    paginator = Paginator(users, 5)  # 5 utilisateurs / page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "users": page_obj,
        "search": search,
        "role": role,
        "status": status,
    }

    return render(request, "administrateur/admin_users.html", context)


# =====================
# AUTRES VUES UTILISATEUR
# =====================
@login_required
def dashboard(request):
    return render(request, 'utilisateurs/dashboard.html')


@login_required
def courses_available(request):
    return render(request, 'utilisateurs/courses_available.html')


@login_required
def profil(request):
    return render(request, 'utilisateurs/profile.html')


@login_required
def cours(request):
    return render(request, 'utilisateurs/cours.html')


@login_required
def historique(request):
    return render(request, 'utilisateurs/historique.html')
