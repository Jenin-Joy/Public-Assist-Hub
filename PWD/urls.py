from django.urls import path
from PWD import views
app_name = "PWD"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),   
]