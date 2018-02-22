from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.urls import reverse
from LH_project.settings import AUTH_USER_MODEL
from datetime import datetime

# Create your models here.


class EmployeeManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class Employee(AbstractUser):

    TYPE_CHOICES = (
        ('DIRECTEUR', 'DIRECTEUR'),
        ('OUVRIER', 'OUVRIER'),
        ('CHEF', 'CHEF'),
    )
    matricule = models.CharField(max_length=25, null=True, blank=False, unique=True)
    cnss = models.CharField(max_length=25, null=True, blank=False)
    service = models.CharField(max_length=25, null=True, blank=True)
    post = models.CharField(max_length=25, null=True, blank=True)
    chef1 = models.ForeignKey(AUTH_USER_MODEL, related_name='subordonne1', on_delete=models.CASCADE, null=True, blank=True)
    chef2 = models.ForeignKey(AUTH_USER_MODEL, related_name='subordonne2', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='OUVRIER')
    nombreConge = models.IntegerField(default=0)
    calculconge = models.IntegerField(default=-1)


    def save(self, *args, **kwargs):
        if self.calculconge == -1 and self.nombreConge != 0:
            self.calculconge = self.nombreConge
        super(Employee, self).save(*args, **kwargs)

    objects = EmployeeManager()


class VacationModel(models.Model):
    NATURE_CHOICES = (
        ('MALADIE', 'MALADIE'),
        ('ROPOS', 'ROPOS'),
        ('PROBLEMES', 'PROBLEMES'),
    )
    VALIDE_CHOICES = [
        ('VALIDE', 'VALIDE'),
        ('ANNULER', 'ANNULER'),
    ]
    par = models.CharField(max_length=80, null=True)
    employee = models.ForeignKey(Employee, related_name='vacations', on_delete=models.CASCADE)
    dateDebut = models.DateField(null=True, blank=False)
    dateFin = models.DateField(null=True, blank=False)
    nature = models.CharField(max_length=20,choices=NATURE_CHOICES, null=True, blank=True, default='R')
    valide = models.CharField(max_length=20, choices=VALIDE_CHOICES, default='EN COURS')
    timeStamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nature

    def get_absolute_url(self):
        return reverse('home')

    def save(self, *args, **kwargs):
        if self.valide == 'VALIDE':
            #print(get_username())
            e = Employee.objects.get(id=self.employee_id)
            fmt = '%Y-%m-%d'
            dd = datetime.strptime(str(self.dateDebut), fmt)
            df = datetime.strptime(str(self.dateFin), fmt)
            dateDiff = (df - dd).days
            e.calculconge = e.calculconge - dateDiff
            e.save()
        super(VacationModel, self).save(*args, **kwargs)


class VacationEdit(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    edited_year = models.IntegerField(default=0)
