from django.db import models
from django.contrib import admin

class Songs(models.Model):
    sid = models.CharField(max_length=100,primary_key=True)
    artist = models.CharField(max_length=200)
    song = models.CharField(max_length=200)
    first = models.CharField(max_length=200)
    second = models.CharField(max_length=200)

class Artist(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    era  = models.CharField(max_length=200)
    origin  = models.CharField(max_length=200)
    genre  = models.CharField(max_length=200)
    mood  = models.CharField(max_length=200)
    img  = models.CharField(max_length=200)
