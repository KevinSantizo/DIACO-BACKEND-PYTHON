from rest_framework import serializers
import locale
from complain.models import Company, StoreBranch, Complain, City, Town, Region, Profile
import datetime
from rest_framework.response import Response


# get only companies
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# get regions
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


# get store branches
class StoreBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreBranch
        fields = '__all__'


# get complains
class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'
        depth = 4


# get cities
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        depth = 2


class StoresWithComplainsCountSerializer(serializers.ModelSerializer):
    complains = serializers.SerializerMethodField('count_complains')

    def count_complains(self, store_branch):
        sch = Complain.objects.filter(store_branch=store_branch).count()
        return sch

    class Meta:
        model = StoreBranch
        fields = ['id', 'name_store_branch', 'address', 'complains', 'company', 'store_branch_town']


class StoresWithChildrenSerializer(serializers.ModelSerializer):
    complains = serializers.SerializerMethodField('get_complains')
    total_complains = serializers.SerializerMethodField('count_complains')

    def get_complains(self, store_branch):
        sch = Complain.objects.filter(store_branch=store_branch)
        serializer = ComplainSerializer(instance=sch, many=True)
        return serializer.data

    def count_complains(self, store_branch):
        sch = Complain.objects.filter(store_branch=store_branch).count()
        return sch

    class Meta:
        model = StoreBranch
        fields = ['id', 'name_store_branch', 'address', 'total_complains', 'complains', 'company', 'store_branch_town']
        depth = 3


# get Towns
class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = '__all__'
        depth = 2


class TownWithChildrenSerializer(serializers.ModelSerializer):
    stores = serializers.SerializerMethodField('get_stores')
    total_stores = serializers.SerializerMethodField('count_stores')
    total_complains = serializers.SerializerMethodField('count_complains')

    def get_stores(self, town):
        sch = StoreBranch.objects.filter(store_branch_town=town)
        serializer = StoresWithComplainsCountSerializer(instance=sch, many=True)
        return serializer.data

    def count_stores(self, town):
        sch = StoreBranch.objects.filter(store_branch_town=town).count()
        return sch

    def count_complains(self, town):
        sch = Complain.objects.filter(store_branch__store_branch_town=town).count()
        return sch

    class Meta:
        model = Town
        fields = ('id', 'city', 'name_town', 'total_stores', 'total_complains', 'stores')
        depth = 2


class CommercesWithChildrenSerializer(serializers.ModelSerializer):
    stores = StoresWithChildrenSerializer(many=True)
    total_complains = serializers.SerializerMethodField("count_complains")

    def count_complains(self, commerce):
        sch = Complain.objects.filter(store_branch__company=commerce).count()
        return sch

    class Meta:
        model = Company
        fields = ('id', 'total_complains', 'name_company', 'phone_company', 'email_company', 'stores')
        depth = 2


class CitiesWithChildrenSerializer(serializers.ModelSerializer):
    towns = serializers.SerializerMethodField('get_towns')
    total_towns = serializers.SerializerMethodField('count_towns')
    total_stores = serializers.SerializerMethodField('count_stores')
    complains = serializers.SerializerMethodField('count_complains')
    stores = serializers.SerializerMethodField('get_stores')
    #

    def get_towns(self, city):
        sch = Town.objects.filter(city=city)
        serializer = TownWithChildrenSerializer(instance=sch, many=True)
        return serializer.data

    def count_towns(self, city):
        sch = Town.objects.filter(city=city).count()
        return sch

    def count_stores(self, city):
        sch = StoreBranch.objects.filter(store_branch_town__city=city).count()
        return sch

    def count_complains(self, city):
        sch = Complain.objects.filter(store_branch__store_branch_town__city=city).count()
        return sch

    def get_stores(self, city):
        sch = StoreBranch.objects.filter(store_branch_town__city=city)
        serializer = StoresWithComplainsCountSerializer(instance=sch, many=True)
        return serializer.data

    class Meta:
        model = City
        fields = ['id', 'name_city', 'total_stores', 'complains', 'region', 'total_towns', 'towns', 'stores']


class RegionsWithChildrenSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField('get_cities')
    total_cities = serializers.SerializerMethodField('count_cities')
    stores = serializers.SerializerMethodField('count_stores')
    complains = serializers.SerializerMethodField('count_complains')

    def get_cities(self, region):
        sch = City.objects.filter(region=region)
        serializer = CitiesWithChildrenSerializer(instance=sch, many=True)
        return serializer.data

    def count_cities(self, region):
        sch = City.objects.filter(region=region).count()
        return sch

    def count_stores(self, region):
        sch = StoreBranch.objects.filter(store_branch_town__city__region=region).count()
        return sch

    def count_complains(self, region):
        sch = Complain.objects.filter(store_branch__store_branch_town__city__region=region).count()
        return sch

    class Meta:
        model = Region
        fields = ['id', 'name_region', 'stores',  'total_cities', 'complains', 'cities']


class GroupDataSerializer(serializers.ModelSerializer):
    complains = serializers.SerializerMethodField(method_name='get_complains')
    month_year = serializers.SerializerMethodField(method_name='get_month_year')
    total = serializers.SerializerMethodField(method_name='get_count_complains')

    # locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    class Meta:
        model = Complain
        fields = ('month_year', 'total', 'complains')

    def get_count_complains(self, instance):
        org_date = str(instance['date_complain'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d")
        month = date.month
        year = date.year
        count = Complain.objects.filter(date_complain__month=month, date_complain__year=year).count()
        return count

    def get_month_year(self, instance):
        org_date = str(instance['date_complain'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d").date()
        month_year = str(date.strftime('%B')) + '-' + str(date.year)
        return str(month_year)

    def get_complains(self, instance):
        org_date = str(instance['date_complain'])
        date = datetime.datetime.strptime(org_date, "%Y-%m-%d")
        month = date.month
        year = date.year
        complains = Complain.objects.filter(date_complain__month=month, date_complain__year=year)
        complain_serializer = ComplainSerializer(complains, many=True)

        return complain_serializer.data


class AddComplainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'


class AddTownsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = '__all__'


class CommercesWithComplainsSerializer(serializers.ModelSerializer):
    total_complains = serializers.SerializerMethodField("count_complains")

    def count_complains(self, commerce):
        sch = Complain.objects.filter(store_branch__company=commerce).count()
        return sch

    class Meta:
        model = Company
        fields = ('id', 'name_company', 'total_complains')


class ProfileSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = Profile.objects.create_user(**validated_data)
        # instance.groups.add('Users')
        return instance

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'username', 'permissions', 'phone', 'email', 'password')