from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('mes-cours/', views.mes_cours, name='mes_cours'),  # avec tiret, pas underscore
    path('calendrier/', views.calendrier, name='calendrier'),  # ← Nouvelle ligne
    path('progression/', views.progression, name='progression'),
    path('communaute/', views.communaute, name='communaute'),
    path('certifications/', views.certifications, name='certifications'),
    path('parametres/', views.parametres, name='parametres'),

# ============================================
# VUES ADMINISTRATEUR
# ============================================
    path('administrateur/courses/', views.admin_courses, name='administrateur_courses'),
    path('administrateur/users/', views.admin_users, name='administrateur_users'),
    path('administrateur/dashboard/', views.admin_dashboard, name='administrateur_dashboard'),

# ============================================
# VUES UTILISATEUR
# ============================================

    path('dashboard/', views.dashboard, name='utilisateur_dashboard'),
    path('courses/', views.courses_available, name='courses_available'),
    path('profil/', views.profil, name='profil'),
    path('cours/', views.cours, name='cours'),
    path('historique/', views.historique, name='historique'),

]
