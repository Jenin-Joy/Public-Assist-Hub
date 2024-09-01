from django.urls import path
from PWD import views
app_name = "PWD"

urlpatterns = [
    # Home Page
    path("homepage/",views.homepage,name="homepage"),  

    # Profile
    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"), 
    path("changepassword/",views.changepassword,name="changepassword"), 
]