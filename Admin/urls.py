from django.urls import path
from Admin import views
app_name = "Admin"
urlpatterns = [
    # Home Page
    path('homepage/',views.homepage,name="homepage"),
    
    # district
    path('district/',views.district,name="district"),
    path('deletedistrict/<str:did>',views.deletedistrict,name="deletedistrict"),
    path('editdistrict/<str:eid>',views.editdistrict,name="editdistrict"),

    # place
    path('place/',views.place,name="place"),
    path('deleteplace/<str:pid>',views.deleteplace,name="deleteplace"),
    path('editplace/<str:pid>',views.editplace,name="editplace"),

    # local place
    path('localplace/',views.localplace,name="localplace"),
    path('deletelocplace/<str:locid>',views.deletelocplace,name="deletelocplace"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),

    # admin registration
    path('adminreg/', views.adminreg,name="adminreg"),
    path('deleteadmin/<str:did>', views.deleteadmin,name="deleteadmin"),

    # Municipality Verification
    path('newmunicipality/',views.newmunicipality,name="newmunicipality"),
    path('municipalityverification/<str:id>/<int:status>', views.municipalityverification,name="municipalityverification"),
    path('approvedmunicipality/',views.approvedmunicipality,name="approvedmunicipality"),
    path('rejectedmunicipality/',views.rejectedmunicipality,name="rejectedmunicipality"),

    # Kseb Verification
    path('newkseb/',views.newkseb,name="newkseb"),
    path('ksebverification/<str:id>/<int:status>', views.ksebverification,name="ksebverification"),
    path('approvedkseb/',views.approvedkseb,name="approvedkseb"),
    path('rejectedkseb/',views.rejectedkseb,name="rejectedkseb"),

    # Mvd Verification
    path('newmvd/',views.newmvd,name="newmvd"),
    path('mvdverification/<str:id>/<int:status>', views.mvdverification,name="mvdverification"),
    path('approvedmvd/',views.approvedmvd,name="approvedmvd"),
    path('rejectedmvd/',views.rejectedmvd,name="rejectedmvd"),

    # Pwd Verification
    path('newpwd/',views.newpwd,name="newpwd"),
    path('pwdverification/<str:id>/<int:status>', views.pwdverification,name="pwdverification"),
    path('approvedpwd/',views.approvedpwd,name="approvedpwd"),
    path('rejectedpwd/',views.rejectedpwd,name="rejectedpwd"),

    # Complaint
    path('complaint/',views.complaint,name="complaint"),
    path('reply/<str:id>',views.reply,name="reply"),
    path('replyedcomplaint/',views.replyedcomplaint,name="replyedcomplaint"),

    # FeedBack
    path('viewfeedback/',views.viewfeedback,name="viewfeedback"),

    #Logout
    path("logout/", views.logout, name="logout"),

]