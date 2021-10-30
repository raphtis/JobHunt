from django.urls import path     
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register), 
    path('login', views.login),
    path('profile', views.profile),
    path('logout', views.logout),

    path('jobs', views.jobs),
    path('create_entry', views.create_entry),
    path('addlisting', views.addlisting),
    path('users/<int:user_id>', views.user), 
    path('jobs/<int:job_id>/edit', views.edit_entry), 
    path('jobs/<int:job_id>/update', views.update),
    path('jobs/<int:job_id>/delete', views.delete),
]