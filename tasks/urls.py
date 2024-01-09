from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/completed", views.completed_tasks, name="completed_tasks"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.task_details, name="task_details"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="complete_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
]
