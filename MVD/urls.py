from django.urls import path
from MVD import views
app_name = "MVD"

urlpatterns = [
    # Homepage
    path("homepage/",views.homepage,name="homepage"),

    # Profile
    path("profile/",views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),

    # Request
    path("viewrequest/",views.viewrequest,name="viewrequest"), 
    path("reply/<str:id>",views.reply,name="reply"), 
    path("replyedrequest/",views.replyedrequest,name="replyedrequest"), 
]