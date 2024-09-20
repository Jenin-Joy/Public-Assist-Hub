from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
# Create your views here.

db = firestore.client()

# convert data into dictionary
def getData(data):
    datas = []
    for i in data:
        datas.append({"data":i.to_dict(),"id":i.id})
    return datas

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

# Request
def viewrequest(request):
    requestdata = []
    req = db.collection("tbl_request").where("pwd_id", "==", request.session["pwdid"]).where("request_status", "==", 0).stream()
    for r in req:
        req = r.to_dict()
        user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
        requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
    return render(request,"PWD/View_Request.html",{"request":requestdata})

def reply(request, id):
    if request.method == "POST":
        req = db.collection("tbl_request").document(id).update({"request_reply":request.POST.get("txt_reply"),"request_status":1})
        return render(request,"Pwd/Reply.html",{"msg":"Reply Send Successfully"})
    else:
        return render(request,"Pwd/Reply.html")

def replyedrequest(request):
    requestdata = []
    req = db.collection("tbl_request").where("pwd_id", "==", request.session["pwdid"]).where("request_status", "==", 1).stream()
    for r in req:
        req = r.to_dict()
        user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
        requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
    return render(request,"PWD/Replyed_Request.html",{"request":requestdata})

# Complaint
def complaint(request):
    complaint = db.collection("tbl_complaint").where("pwd_id", "==", request.session["pwdid"]).stream()
    complaintdata = getData(complaint)
    if request.method == "POST":
        db.collection("tbl_complaint").add({"complaint_title":request.POST.get("txt_title"),
                                            "complaint_content":request.POST.get("txt_content"),
                                            "complaint_date":datetime.now(),
                                            "complaint_reply":"",
                                            "complaint_status":0,
                                            "complaint_photo":"",
                                            "user_id":"",
                                            "municipality_id":"",
                                            "kseb_id":"",
                                            "pwd_id":request.session["pwdid"],
                                            "mvd_id":""})
        return render(request,"PWD/Complaint.html",{"msg":"Complaint Send Sucessfully"})
    else:
        return render(request,"PWD/Complaint.html",{"complaint":complaintdata})