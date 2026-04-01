from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage_teacher/', views.manage_teacher, name='manage_teacher'),
    path('save_teacher/', views.save_teacher, name='save_teacher'),
    path('edit_teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('view_users/', views.view_users, name='view_users'),
    path('statistics/', views.statistics, name='statistics'),
    path('export_csv/', views.export_teachers_csv, name='export_teachers_csv'),
    path('import_csv/', views.import_teachers_csv, name='import_teachers_csv'),
]