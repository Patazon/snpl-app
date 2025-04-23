from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse


# Create your views here.
def login_user(request):

    # if they submit the form
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect(reverse("login"))

    else:
        return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)

    messages.success(request, "Till next time...")

    return redirect("login")
