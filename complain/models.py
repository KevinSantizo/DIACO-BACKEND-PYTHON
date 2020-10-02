from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Company(models.Model):
    name_company = models.CharField(max_length=100)
    phone_company = models.CharField(max_length=15)
    email_company = models.EmailField(unique=True)

    def __str__(self):
        return self.name_company


class Region(models.Model):
    name_region = models.CharField(max_length=100)

    def __str__(self):
        return self.name_region


class StoreBranch(models.Model):
    company = models.ForeignKey(Company, related_name='stores', on_delete=models.CASCADE, null=True)
    store_branch_town = models.ForeignKey('Town', related_name='town_stores', on_delete=models.CASCADE, null=True)
    name_store_branch = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name_store_branch + ' - ' + self.company.name_company + ' - ' + self.store_branch_town.name_town + ' - ' + self.store_branch_town.city.name_city + ' - ' + self.store_branch_town.city.region.name_region


class Complain(models.Model):
    store_branch = models.ForeignKey(StoreBranch, related_name='complains', on_delete=models.CASCADE, null=True)
    name_complain = models.CharField(max_length=100)
    description_complain = models.CharField(max_length=100)
    date_complain = models.DateField()

    def __str__(self):
        return self.name_complain + ' ' + str(self.date_complain) + ' ' + self.store_branch.name_store_branch + ' ' + self.store_branch.store_branch_town.name_town


class City(models.Model):
    region = models.ForeignKey(Region, related_name='cities', on_delete=models.CASCADE, null=True)
    name_city = models.CharField(max_length=100)

    def __str__(self):
        return self.name_city + ' - ' + self.region.name_region


class Town(models.Model):
    city = models.ForeignKey(City, related_name='towns', on_delete=models.CASCADE, null=True)
    name_town = models.CharField(max_length=100)

    def __str__(self):
        return self.name_town + ' - ' + self.city.name_city + ' - ' + self.city.region.name_region


class Profile(AbstractUser):
    phone = models.CharField(max_length=50, null=True)
    PERMISSIONS = (
        ('0', 'Collaborator'),
        ('1', 'Admin'),
    )
    permissions = models.CharField(
        max_length=1,
        choices=PERMISSIONS,
        blank=True,
        default='0',
    )

    def __str__(self):
        return self.username