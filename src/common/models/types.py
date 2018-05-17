from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, models.CASCADE)
    name = models.CharField(max_length=50)


class Type(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, models.CASCADE)
    name = models.CharField(max_length=50)
