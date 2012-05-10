from django.db import models

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

