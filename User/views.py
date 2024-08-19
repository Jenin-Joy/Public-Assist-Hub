from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
# Create your views here.

# Data Base connection
db = firestore.client()

# Home Page Function
def homepage(request):
    return render(request, 'User/Homepage.html')

# profile
def profile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    return render(request, 'User/MyProfile.html',{"user": user})

# Edit profile
def editprofile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_user").document(request.session["uid"]).update({
            "user_name": request.POST.get("txt_name"),
            "user_contact": request.POST.get("txt_contact"),
            "user_address": request.POST.get("txt_address"),
        })
        return render(request, 'User/MyProfile.html',{"msg": "Profile updated"})
    else:
        return render(request, 'User/EditProfile.html',{"user": user})