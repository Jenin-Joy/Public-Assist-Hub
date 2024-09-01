from django.urls import path
from User import views
app_name = "User"

urlpatterns = [
    # Home Page
    path("homepage/",views.homepage,name="homepage"),   

    # Profile
    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

]