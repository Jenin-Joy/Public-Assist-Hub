from django.urls import path
from MVD import views
app_name = "MVD"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
]