from django.db import models
from django.contrib.auth.models import User

class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    trees = models.ManyToManyField('LVATree')
    min_ects = models.DecimalField(max_digits=4, decimal_places=2, null=True)

class LVA(models.Model):
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    ects = models.DecimalField(max_digits=4, decimal_places=2)

class LVATree(models.Model):
    lvas = models.ManyToManyField(LVA)
    subtrees = models.ManyToManyField('LVATree')
    treetype = models.CharField(max_length=100)
    min_ects = models.DecimalField(max_digits=4, decimal_places=2, null=True)

class Certificate(models.Model):
    lvano = models.CharField(max_length=100)
    lvatype = models.CharField(max_length=100)
    lvaname = models.CharField(max_length=100)
    semst = models.DecimalField(max_digits=4,decimal_places=2)
    ects = models.DecimalField(max_digits=4,decimal_places=2)
    date = models.CharField(max_length=100)
    curriculum = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    professor = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    use_for = models.ForeignKey(Curriculum, null=True, blank=True)

