from django.shortcuts import redirect
from backend.models import Entry
from datetime import datetime


def edit_entry(request):
    if request.user.is_authenticated:
        id = request.POST.get("id")
        if id:
            entry = Entry.objects.get(id=id, client__owner=request.user)

            start_time = datetime.fromisoformat(request.POST.get("start_time"))

            end_time = datetime.fromisoformat(request.POST.get("end_time"))

            entry.start_time = start_time
            entry.end_time = end_time
            entry.save()

        return redirect("index")


def delete_entry(request):
    if request.user.is_authenticated:
        id = request.GET.get("id")
        if id:
            Entry.objects.filter(id=id, client__owner=request.user).delete()
        return redirect("index")
    return redirect("index")
