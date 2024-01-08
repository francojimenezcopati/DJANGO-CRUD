from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("signout/", views.signout, name="signout"),
    path("signin/", views.signin, name="signin"),
]
