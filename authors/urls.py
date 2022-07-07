from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', view=views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/post/new/',
        views.DashboardPost.as_view(),
        name='dashboard_new_post'),
    path(
        'dashboard/post/delete/',
        views.dashboard_post_delete,
        name='dashboard_post_delete'),
    path(
        'dashboard/post/<int:id>/edit/',
        views.DashboardPost.as_view(),
        name='dashboard_post_edit'),


]
