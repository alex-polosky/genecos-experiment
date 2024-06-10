from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter
from geneco import views

router = SimpleRouter()
router.register('agency', views.AgencyViewSet, basename='agencies')
router.register('contract', views.ContractViewSet, basename='contracts')
router.register('account_consumer', views.AccountConsumerViewSet, basename='account_consumers')
router.register('account', views.AccountViewSet, basename='accounts')
router.register('address_lead', views.AddressLeadViewSet, basename='address_leads')
router.register('client', views.ClientViewSet, basename='clients')
router.register('consumer', views.ConsumerViewSet, basename='consumers')

urlpattens = [
    path('token/', obtain_auth_token),
    path('contract/<uuid:contract>/ingest/', views.AccountIngestView)
] + router.urls
