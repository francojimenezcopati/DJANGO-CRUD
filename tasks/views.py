# --------- AUTH ------------------------------------
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# ---------------------------------------------------
# --------- DJANGO ------------------------------------
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# -----------------------------------------------------

from .forms import TaskForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, "home.html")


# region AUTH

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        datos = request.POST
        if datos["password1"] == datos["password2"]:
            try:
                user = User.objects.create_user(
                    datos["username"], password=datos["password1"]
                )
                user.save()
                login(
                    request, user
                )  # <-- ----------------------------------------------- CREA LA COOKIE PARA LA AUTH DEL USUARIO
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm,
                        "error": "Username already exists",
                    },
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "Passwords do not match"},
            )


def signin(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        datos = request.POST
        user = authenticate(
            request, username=datos["username"], password=datos["password"]
        )
        if user:
            login(request, user)
            return redirect("tasks")
        else:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )

@login_required
def signout(request):
    logout(request)
    return redirect("home")


# endregion

# region Tasks

@login_required
def tasks(request):
    tasks = list(
        Task.objects.filter(user=request.user, datecompleted__isnull=True)
    )
    return render(request, "tasks/tasks.html", {"tasks": tasks})


@login_required
def completed_tasks(request):
    tasks = list(
        Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    )
    return render(request, "tasks/tasks.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "tasks/create_task.html", {"form": TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "tasks/create_task.html",
                {"form": TaskForm(), "error": "Please provide valid data"},
            )


@login_required
def task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "GET":
        form = TaskForm(instance=task)
        return render(request, "tasks/task_details.html", {"form": form, 'task': task})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "tasks/task_details.html",
                {"form": TaskForm(), "error": "Please provide valid data", 'task': task},
            )


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')


# endregion
