from django.urls import path
from rest_framework.authtoken import views
from .views import *


urlpattens = [
    path('token/', views.obtain_auth_token),
    path('contract/<uuid:contract>/ingest/', AccountIngestView)
]
