from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.contract_list),
    path('create/', views.contract_create, name="create"),
]
