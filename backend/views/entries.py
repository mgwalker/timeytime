from django.shortcuts import redirect
from backend.models import Entry
from datetime import datetime
from django.utils.timezone import UTC


def edit_entry(request):
    if request.user.is_authenticated:
        id = request.POST.get("id")
        if id:
            current_entry = Entry.objects.get(id=id, client__owner=request.user)
            edited_entry = Entry.objects.get(id=id, client__owner=request.user)

            # Remove the PK and update the state in order to essentially clone
            # the current entry into a new one.
            edited_entry.pk = None
            edited_entry._state.adding = True

            print(request.POST)
            # Update the start and end time of the new entry
            edited_entry.start_time = datetime.fromisoformat(
                request.POST.get("start_time")
            )
            # End time is not strictly required. The user could be updating
            # the start time of the currently-active entry
            if request.POST.get("end_time"):
                edited_entry.end_time = datetime.fromisoformat(
                    request.POST.get("end_time")
                )

            # Cross-link the old and new entries
            edited_entry.editedfrom = current_entry
            current_entry.editedto = edited_entry

            # Saaaaave
            edited_entry.save()
            current_entry.save()

        return redirect("index")


def delete_entry(request):
    if request.user.is_authenticated:
        id = request.GET.get("id")
        if id:
            entry = Entry.objects.get(id=id, client__owner=request.user)
            if not entry.end_time:
                entry.end_time = datetime.utcnow().replace(tzinfo=UTC)
            entry.deleted = True
            entry.save()
        return redirect("index")
    return redirect("index")
