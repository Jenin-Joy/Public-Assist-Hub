from django.urls import path
from Guest import views
app_name = "Guest"

urlpatterns = [
    path("municipality/", views.municipality, name="municipality"), 

    path("user/", views.user, name="user"),   
    path("ajaxmunicipality/", views.ajaxmunicipality, name="ajaxmunicipality"),   
    path("ajaxlocalplace/", views.ajaxlocalplace, name="ajaxlocalplace"), 

    path("pwd/", views.pwd, name="pwd"), 
    path("mvd/", views.mvd, name="mvd"), 
    path("kseb/", views.kseb, name="kseb"), 
]