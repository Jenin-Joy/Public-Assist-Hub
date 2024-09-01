from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
# Create your views here.

db = firestore.client()

# Homepage
def homepage(request):
    return render(request, 'MVD/Homepage.html')

# profile
def profile(request):
    mvd = db.collection("tbl_mvd").document(request.session["mvdid"]).get().to_dict()
    return render(request, 'mvd/MyProfile.html',{"mvd": mvd})

# Edit profile
def editprofile(request):
    mvd = db.collection("tbl_mvd").document(request.session["mvdid"]).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_mvd").document(request.session["mvdid"]).update({
            "mvd_name": request.POST.get("txt_name"),
            "mvd_contact": request.POST.get("txt_contact"),
            "mvd_address": request.POST.get("txt_address"),
        })
        return render(request, 'mvd/MyProfile.html',{"msg": "Profile updated"})
    else:
        return render(request, 'mvd/EditProfile.html',{"mvd": mvd})

# Change Password
def changepassword(request):
    mvd = db.collection("tbl_mvd").document(request.session["mvdid"]).get().to_dict()
    email = mvd["mvd_email"]
    # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Public Assist Hub site password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"mvd/HomePage.html",{"msg1":email})