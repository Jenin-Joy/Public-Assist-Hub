from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
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

# Change Password
def changepassword(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]
    # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Public Assist Hub site password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"User/HomePage.html",{"msg1":email})