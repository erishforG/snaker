from __future__ import unicode_literals

from django.db import models

class analytics(models.Model):
    id = models.AutoField(primary_key=True)
    url_id = models.IntegerField()
    created_at = models.DateTimeField()
    os = models.CharField(max_length=64, blank=True, null=True)
    browser = models.CharField(max_length=256, blank=True, null=True)
    device = models.CharField(max_length=64, blank=True, null=True)
    referer = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analytics'


class count(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.IntegerField()
    url_id = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'count'


class media(models.Model):
    id = models.AutoField(primary_key=True)
    shown_name = models.CharField(unique=True, max_length=64)
    name = models.CharField(unique=True, max_length=64)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'media'


class url(models.Model):
    id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=32)
    long_url = models.CharField(db_column='longUrl', max_length=2048, blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    type = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    show_redirection = models.IntegerField(db_column='showRedirection', default=0)
    show_utm = models.IntegerField(db_column='showUtm', default=1)
    created_at = models.DateTimeField()
    tags = models.CharField(max_length=32, null=True)

    class Meta:
        managed = False
        db_table = 'url'

    def tags_to_bool_array(self):
        if self.tags is None:
            return []
        str_arr = self.tags.split(',')
        return str_arr


    def all_tag_array(self):
        if self.tags is None:
            return [False] * 8
        arr = []
        str_arr = self.tags.split(',')
        for i in range(1, 9):
            arr.append(i in str_arr)
        return arr



class url_link(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=2048)
    created_at = models.DateTimeField()
    media_id = models.IntegerField()
    url_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'url_link'
        unique_together = (('url_id', 'media_id'))