from django.urls import path
from Municipality import views
app_name = "Municipality"

urlpatterns = [
    path("homepage/",views.homepage,name="homepage"),
]