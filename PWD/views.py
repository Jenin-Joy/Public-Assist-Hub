from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
# Create your views here.

db = firestore.client()

# Home Page
def homepage(request):
    return render(request, 'pwd/Homepage.html')

# profile
def profile(request):
    pwd = db.collection("tbl_pwd").document(request.session["pwdid"]).get().to_dict()
    return render(request, 'pwd/MyProfile.html',{"pwd": pwd})

# Edit profile
def editprofile(request):
    pwd = db.collection("tbl_pwd").document(request.session["pwdid"]).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_pwd").document(request.session["pwdid"]).update({
            "pwd_name": request.POST.get("txt_name"),
            "pwd_contact": request.POST.get("txt_contact"),
            "pwd_address": request.POST.get("txt_address"),
        })
        return render(request, 'pwd/MyProfile.html',{"msg": "Profile updated"})
    else:
        return render(request, 'pwd/EditProfile.html',{"pwd": pwd})

# Change Password
def changepassword(request):
    pwd = db.collection("tbl_pwd").document(request.session["pwdid"]).get().to_dict()
    email = pwd["pwd_email"]
    # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Public Assist Hub site password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"PWD/HomePage.html",{"msg1":email})