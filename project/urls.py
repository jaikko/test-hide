from django.urls import path, include
from project.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename="Client")
contract_routeur = routers.NestedSimpleRouter(router, r'clients', lookup='client')
contract_routeur.register(r'contracts', ContractViewSet, basename='client-contracts')
event_routeur = routers.NestedSimpleRouter(contract_routeur, r'contracts', lookup='contract')
event_routeur.register(r'events', EventViewSet, basename='contract-events')
status = routers.DefaultRouter()
status.register(r'status', StatusViewSet, basename="status")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(contract_routeur.urls)),
    path('', include(event_routeur.urls)),
    path('', include(status.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
