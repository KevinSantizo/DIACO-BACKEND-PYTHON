from rest_framework import routers
from django.urls import path, include

from complain.views import (
    CompanyViewSet,
    RegionViewSet,
    StoreBranchViewSet,
    ComplainViewSet,
    CityViewSet,
    TownViewSet,
    CommercesWithChildrenViewSet,
    CitiesWithChildrenViewSet,
    RegionsWithChildrenViewSet,
    ComplainsCommerce,
    GroupDataView,
    ComplainRegion,
    StoresWithChildrenViewSet,
    AddComplainsViewSet,
    AddTownsViewSet,
    TownsWithChildrenViewsSet,
    CommercesWithComplainsViewSet,
    UserViewSet
    # RegionCommercesStores
)

router = routers.SimpleRouter()
router.register('companies', CompanyViewSet)
router.register('regions', RegionViewSet)
router.register('store-branches', StoreBranchViewSet)
router.register('complains', ComplainViewSet)
router.register('cities', CityViewSet)
router.register('towns', TownViewSet)
router.register('commerces-stores', CommercesWithChildrenViewSet)
router.register('cities-children', CitiesWithChildrenViewSet)
router.register('regions-children', RegionsWithChildrenViewSet)
router.register('stores-children', StoresWithChildrenViewSet)
router.register('add-complains', AddComplainsViewSet)
router.register('add-towns', AddTownsViewSet)
router.register('tows-children', TownsWithChildrenViewsSet)
router.register('commerces-complains', CommercesWithComplainsViewSet)
router.register('users', UserViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('report-complains/', ComplainsCommerce.as_view(), name='report-complains'),
    path('data-group/', GroupDataView.as_view(), name='data-group'),
    path('complains-region/', ComplainRegion.as_view(), name='complains-region'),
    # path('regions-stores/', RegionCommercesStores.as_view(), name='regions-stores'),
]