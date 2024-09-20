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

# Request
def viewrequest(request):
    requestdata = []
    req = db.collection("tbl_request").where("kseb_id", "==", request.session["ksebid"]).where("request_status", "==", 0).stream()
    for r in req:
        req = r.to_dict()
        user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
        requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
    return render(request,"KSEB/View_Request.html",{"request":requestdata})

def reply(request, id):
    if request.method == "POST":
        req = db.collection("tbl_request").document(id).update({"request_reply":request.POST.get("txt_reply"),"request_status":1})
        return render(request,"KSEB/Reply.html",{"msg":"Reply Send Successfully"})
    else:
        return render(request,"KSEB/Reply.html")

def replyedrequest(request):
    requestdata = []
    req = db.collection("tbl_request").where("kseb_id", "==", request.session["ksebid"]).where("request_status", "==", 1).stream()
    for r in req:
        req = r.to_dict()
        user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
        requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
    return render(request,"KSEB/Replyed_Request.html",{"request":requestdata})