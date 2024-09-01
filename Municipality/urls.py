from django.urls import path
from Municipality import views
app_name = "Municipality"

urlpatterns = [
    # Homepage
    path("homepage/",views.homepage,name="homepage"),

    # Profile
    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
]