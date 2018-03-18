from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class user(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    user_id = models.CharField(max_length=255)
    # base64
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def publish(self):
        self.save()

    class Meta:
        managed = False
        db_table = 'user'