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

    # Complaint
    path("complaint/", views.complaint, name="complaint"),

    # View Complaint
    path("viewcomplaint/", views.viewcomplaint, name="viewcomplaint"),
    path("replytocomplaint/<str:id>", views.replytocomplaint, name="replytocomplaint"),
    path("replyedcomplaint/", views.replyedcomplaint, name="replyedcomplaint"),

    #FeedBack
    path("feedback/", views.feedback, name="feedback"),

    # View Post
    path('ajaxlike/',views.ajaxlike,name="ajaxlike"),
    path('ajaxcomment/',views.ajaxcomment,name="ajaxcomment"),
    path('ajaxgetcommant/',views.ajaxgetcommant,name="ajaxgetcommant"),
]