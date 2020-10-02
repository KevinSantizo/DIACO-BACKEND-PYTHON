from django.contrib import admin
from complain.models import Company, StoreBranch, Complain, City, Town, Region, Profile

# Register your models here.
admin.site.register(Profile)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name_company', 'phone_company', 'email_company')


@admin.register(StoreBranch)
class StoreBranchAdmin(admin.ModelAdmin):
    list_display = ('company', 'store_branch_town', 'name_store_branch', 'address')



@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = ('store_branch', 'name_complain', 'description_complain', 'date_complain',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('region', 'name_city')


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ('city', 'name_town')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name_region',)
