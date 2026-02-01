from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import UTC
from datetime import datetime
from backend.util import isto_quick_timestamp


def _utc_now():
    return datetime.utcnow().replace(tzinfo=UTC)


class Client(models.Model):
    name = models.TextField(null=False)
    description = models.TextField(null=True, default=None)
    color = models.CharField(max_length=7, null=True, default=None)
    timezone = models.TextField(null=True, default=None)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)


class Entry(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(default=_utc_now)
    end_time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, default=None)
    editedfrom = models.ForeignKey(
        "self",
        related_name="edited_from",
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
    )
    editedto = models.ForeignKey(
        "self",
        related_name="edited_to",
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
    )
    deleted = models.BooleanField(default=False)

    @property
    def active(self):
        return self.end_time is None

    @classmethod
    def start(cls, id):
        cls.stop()
        client = Client.objects.get(id=id)
        cls.objects.create(client=client)

        if client.name == "Illinois Treasurer":
            isto_quick_timestamp()

    @classmethod
    def stop(cls):
        active = cls.objects.filter(end_time=None).first()
        if active:
            if active.client.name == "Illinois Treasurer":
                isto_quick_timestamp()

            active.end_time = datetime.utcnow().replace(tzinfo=UTC)
            active.save()
