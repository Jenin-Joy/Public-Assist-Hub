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

    # Search PWD
    path("searchpwd/", views.searchpwd, name="searchpwd"),
    path("ajaxsearchpwd/", views.ajaxsearchpwd, name="ajaxsearchpwd"),

    # Search MVD
    path("searchmvd/", views.searchmvd, name="searchmvd"),
    path("ajaxsearchmvd/", views.ajaxsearchmvd, name="ajaxsearchmvd"),

    # Search Municipality
    path("searchmunicipality/", views.searchmunicipality, name="searchmunicipality"),
    path("ajaxsearchmunicipality/", views.ajaxsearchmunicipality, name="ajaxsearchmunicipality"),

    # Search Kseb
    path("searchKseb/", views.searchKseb, name="searchKseb"),
    path("ajaxsearchkseb/", views.ajaxsearchkseb, name="ajaxsearchkseb"),

    # Mvd Request
    path("mvdrequest/<str:id>", views.mvdrequest, name="mvdrequest"),

    # Kseb Request
    path("ksebrequest/<str:id>", views.ksebrequest, name="ksebrequest"),

    # Pwd Request
    path("pwdrequest/<str:id>", views.pwdrequest, name="pwdrequest"),

    # Municipality Request
    path("municipalityrequest/<str:id>", views.municipalityrequest, name="municipalityrequest"),

    # My Request
    path("myrequest/", views.myrequest, name="myrequest"),

    # Complaint
    path("complaint/", views.complaint, name="complaint"),

    # Official Complaint Municipality
    path("OfficalComplaintMunicipality/<str:id>", views.OfficalComplaintMunicipality, name="OfficalComplaintMunicipality"),

    # Official Complaint Mvd
    path("OfficalComplaintMvd/<str:id>", views.OfficalComplaintMvd, name="OfficalComplaintMvd"),

    # View Offical Complaints
    path("viewofficialcomplaints/", views.viewofficialcomplaints, name="viewofficialcomplaints"),

    # Add Post
    path("addpost/", views.addpost, name="addpost"),
    path("deletepost/<str:id>", views.deletepost, name="deletepost"),

    # View Post
    path('ajaxlike/',views.ajaxlike,name="ajaxlike"),
    path('ajaxcomment/',views.ajaxcomment,name="ajaxcomment"),
    path('ajaxgetcommant/',views.ajaxgetcommant,name="ajaxgetcommant"),

    #FeedBack
    path("feedback/", views.feedback, name="feedback"),

]