# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ScraperBinnacle(models.Model):
    url = models.CharField(max_length=100)
    total_data = models.IntegerField(default=0, blank=True, null=True)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)