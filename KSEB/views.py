from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
# Create your views here.

db = firestore.client()

# Homepage
def homepage(request):
    return render(request, 'KSEB/Homepage.html')

# profile
def profile(request):
    kseb = db.collection("tbl_kseb").document(request.session["ksebid"]).get().to_dict()
    return render(request, 'kseb/MyProfile.html',{"kseb": kseb})

# Edit profile
def editprofile(request):
    kseb = db.collection("tbl_kseb").document(request.session["ksebid"]).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_kseb").document(request.session["ksebid"]).update({
            "kseb_name": request.POST.get("txt_name"),
            "kseb_contact": request.POST.get("txt_contact"),
            "kseb_address": request.POST.get("txt_address"),
        })
        return render(request, 'kseb/MyProfile.html',{"msg": "Profile updated"})
    else:
        return render(request, 'kseb/EditProfile.html',{"kseb": kseb})

# Change Password
def changepassword(request):
    kseb = db.collection("tbl_kseb").document(request.session["ksebid"]).get().to_dict()
    email = kseb["kseb_email"]
    # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Public Assist Hub site password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"KSEB/HomePage.html",{"msg1":email})