from django.shortcuts import render, redirect
from backend.models import Client
from django.contrib import messages


def clients(request, **kwargs):
    if request.user.is_authenticated:
        edit = kwargs.get("edit")
        if not edit:
            edit = request.GET.get("edit")

        if edit:
            client = Client.objects.get(id=edit)
            return render(request, "clients.html", {"clients": [], "edit": client})
            pass

        clients = Client.objects.filter(owner=request.user)
        return render(
            request,
            "clients.html",
            {
                "clients": clients,
                "edit": {
                    "color": kwargs.get("color"),
                    "description": kwargs.get("description"),
                },
            },
        )
    return render(request, "index.html")


def add_client(request):
    if request.user.is_authenticated and request.POST:
        post = dict(request.POST)
        if post["name"] and post["name"][0]:
            Client.objects.create(
                name=post["name"][0],
                owner=request.user,
                color=post["color"][0],
                description=post["description"][0],
            )
            print(post["name"])
            return redirect("clients")

        messages.add_message(request, messages.ERROR, "Name is required")
        return clients(
            request, color=post["color"][0], description=post["description"][0]
        )
    return render(request, "index.html")


def edit_client(request):
    if request.user.is_authenticated and request.POST:
        post = dict(request.POST)
        id = post["id"][0] if "id" in post else None
        if "name" in post and post["name"][0] and id:
            edit = Client.objects.get(id=id, owner=request.user)
            edit.name = post["name"][0]
            edit.color = post["color"][0]
            edit.description = post["description"][0]
            edit.timezone = post["timezone"][0]
            edit.save()

            return redirect("clients")

        messages.add_message(request, messages.ERROR, "Name is required")
        return clients(request, edit=id)

    return render(request, "index.html")


def delete_client(request):
    if request.user.is_authenticated:
        id = request.GET.get("id")
        if id:
            Client.objects.filter(id=id, owner=request.user).delete()
        return redirect("clients")
    return render(request, "index.html")
