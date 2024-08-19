from django.urls import path
from KSEB import views
app_name = "KSEB"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
]