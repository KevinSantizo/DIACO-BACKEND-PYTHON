from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from rest_framework import routers
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from complain.models import Company, StoreBranch, Complain, City, Town, Region, Profile
from complain.serializers import (
    CompanySerializer,
    RegionSerializer,
    StoreBranchSerializer,
    ComplainSerializer,
    CitySerializer,
    TownSerializer,
    CommercesWithChildrenSerializer,
    CitiesWithChildrenSerializer,
    RegionsWithChildrenSerializer,
    GroupDataSerializer,
    StoresWithChildrenSerializer,
    AddComplainsSerializer,
    AddTownsSerializer,
    TownWithChildrenSerializer,
    CommercesWithComplainsSerializer,
    ProfileSerializer
)
from .filters import ComplainFilter

from datetime import datetime


class CompanyViewSet(viewsets.ModelViewSet):  # get only companies
    permission_classes = []
    authentication_classes = []
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class RegionViewSet(viewsets.ModelViewSet):  # get only regions
    permission_classes = []
    authentication_classes = []
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class StoreBranchViewSet(viewsets.ModelViewSet):  # get only store branches
    permission_classes = []
    authentication_classes = []
    queryset = StoreBranch.objects.all()
    serializer_class = StoreBranchSerializer


class ComplainViewSet(viewsets.ModelViewSet):  # get only complains
    permission_classes = []
    authentication_classes = []
    queryset = Complain.objects.order_by('-date_complain')
    serializer_class = ComplainSerializer
    filterset_class = ComplainFilter


class CityViewSet(viewsets.ModelViewSet):  # get only complains
    permission_classes = []
    authentication_classes = []
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TownViewSet(viewsets.ModelViewSet):  # get only towns
    permission_classes = []
    authentication_classes = []
    queryset = Town.objects.all()
    serializer_class = TownSerializer


class CommercesWithChildrenViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Company.objects.all()
    serializer_class = CommercesWithChildrenSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'name_company')


class CitiesWithChildrenViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = City.objects.all()
    serializer_class = CitiesWithChildrenSerializer


class RegionsWithChildrenViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Region.objects.all()
    serializer_class = RegionsWithChildrenSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name_region',)


class ComplainsCommerce(APIView):

    def get(self, request, *args, **kwargs):

        today = datetime.now()
        current_year = today.year
        commerces = Company.objects.raw('SELECT * from complain_Company')
        response = {
            "complains_in_south_north": [],
            "complains_in_east": []
        }
        for c in commerces:
            total_complains_commerces_south = 0
            total_complains_commerces_north = 0
            store_branches_east = StoreBranch.objects.filter(company=c, store_branch_town__city__region__name_region='Oriente')
            complains_east = 0
            for s_o in store_branches_east:
                complains_east += Complain.objects.filter(date_complain__year=current_year, store_branch=s_o).count()
            if complains_east == 0:
                store_branches_north = StoreBranch.objects.filter(company=c, store_branch_town__city__region__name_region='Norte')
                store_branches_south = StoreBranch.objects.filter(company=c, store_branch_town__city__region__name_region='Sur')
                for s_o in store_branches_north:
                    total_complains_commerces_north += Complain.objects.filter(date_complain__year=current_year, store_branch=s_o).count()
                for s_o in store_branches_south:
                    total_complains_commerces_south += Complain.objects.filter(date_complain__year=current_year, store_branch=s_o).count()
                    if total_complains_commerces_north > 0 and total_complains_commerces_south > 0:
                        response['complains_in_south_north'].append({
                            "commerce": c.name_company,
                            "complains_south": total_complains_commerces_south,
                            "complains_north": total_complains_commerces_north,
                            'current_year': current_year,
                            "complains_east": 0
                        })
            else:
                response['complains_in_east'].append({
                    "commerce": c.name_company,
                    "complains": complains_east,
                    'current_year': current_year
                })

        return Response(response)


class GroupDataView(ListAPIView):
    permission_classes = []
    authentication_classes = []
    queryset = Complain.objects.all()

    serializer_class = GroupDataSerializer

    def get_queryset(self):
        queryset = self.queryset
        print(datetime.now().date())

        return queryset.annotate(month=TruncMonth('date_complain')).values('date_complain').annotate(c=Count('id')).order_by()


class ComplainRegion(APIView):
    def get(self, request, *args, **kwargs):
        regions = Region.objects.all()

        response = []

        for k in regions:
            print(k)
            total_complains_regions = 0
            total_complains_regions += Complain.objects.filter(store_branch__store_branch_town__city__region__name_region=k).count()

            response.append({
                "region": k.name_region,
                "complains": total_complains_regions
            })
        return Response(response)


# class RegionCommercesStores(APIView):
#
#     def get(self, request, *args, **kwargs):
#         companies = Company.objects.all()
#         response = []
#
#         for j in companies:
#             commerces_region_east = StoreBranch.objects.filter(company=j, store_branch_town__city__region__name_region='Oriente')
#             for c_o in commerces_region_east:
#                 total_commerces_region_east = 0
#                 total_commerces_region_east += StoreBranch.objects.filter(store_branch_town__city__region__name_region=c_o).count()
#
#                 response.append({
#                     "region": c_o.name_region,
#                     "companies": total_commerces_region_east
#                 })
#         return Response(response)

class StoresWithChildrenViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = StoreBranch.objects.all()
    serializer_class = StoresWithChildrenSerializer


class AddComplainsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Complain.objects.all()
    serializer_class = AddComplainsSerializer


class AddTownsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Town.objects.all()
    serializer_class = AddTownsSerializer


class TownsWithChildrenViewsSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Town.objects.all()
    serializer_class = TownWithChildrenSerializer


class CommercesWithComplainsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Company.objects.all()
    serializer_class = CommercesWithComplainsSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer