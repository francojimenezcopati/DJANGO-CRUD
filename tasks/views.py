from django.shortcuts import render, redirect

# --------- AUTH ------------------------------------
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# ---------------------------------------------------
from django.db import IntegrityError

from .forms import CreateNewTaskForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, "home.html")

def tasks(request):
    tasks = list(Task.objects.filter(user=request.user, datecompleted__isnull=True))
    return render(request, "tasks/tasks.html", {
        'tasks': tasks
    })


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

def signout(request):
    logout(request)
    return redirect("home")


def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {'form': CreateNewTaskForm()})
    else:
        try:
            form = CreateNewTaskForm(request.POST)
            new_task = form.save(False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': CreateNewTaskForm(),
                'error': 'Please provide valid data'
            })