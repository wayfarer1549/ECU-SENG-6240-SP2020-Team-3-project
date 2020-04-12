from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.contract_list),
    path('create/', views.contract_create, name="create"),
    re_path('(?P<slug>[\w-]+)/', views.contract_detail, name="detail"),
]
