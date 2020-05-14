from django.db import models
from jsonfield import JSONField


class TicketRecords(models.Model):
    attr = JSONField()
