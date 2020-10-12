from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=100)
  cnpj = models.CharField(max_length=14)

  def __str__(self):
    return self.name

class Employee(models.Model):
  name = models.CharField(max_length=100)
  cpf = models.CharField(max_length=11)

  def __str__(self):
    return self.name