from django.contrib.auth import logout as log_out
from django.shortcuts import render, redirect
from backend.models import Entry


def start_timer(request):
    if request.user.is_authenticated:
        id = request.GET.get("id")
        if id:
            Entry.start(id)
            return redirect("index")

    return render(request, "index.html")


def stop_timer(request):
    if request.user.is_authenticated:
        Entry.stop()
        return redirect("index")

    return render(request, "index.html")


def logout(request):
    log_out(request)
    return redirect("/")
