from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def signup_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login_user")

    return render(request, "accounts/signup_user.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")

    context = {}
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            context = {
                "error": "Username or password is incorrect.",
            }
    return render(request, "accounts/login_user.html", context)


@login_required
def logout_user(request):
    logout(request)
    return redirect("accounts:login_user")
