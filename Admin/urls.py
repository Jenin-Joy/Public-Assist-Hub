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
]