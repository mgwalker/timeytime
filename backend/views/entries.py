from django.shortcuts import redirect
from backend.models import Entry


def delete_entry(request):
    if request.user.is_authenticated:
        id = request.GET.get("id")
        if id:
            Entry.objects.filter(id=id).delete()
        return redirect("index")
    return redirect("index")
