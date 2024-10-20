from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
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
    if "pwdid" in request.session:
        post = db.collection("tbl_post").stream()
        post_data = []
        for i in post:
            likescount = db.collection("tbl_like").where("post_id", "==", i.id).get()
            data_list_count = len(likescount)
            # print(data_list_count)
            ps = i.to_dict()
            pro = db.collection("tbl_user").document(ps["user_id"]).get().to_dict()
            likes = db.collection("tbl_like").where("post_id", "==", i.id).where("pwd_id", "==", request.session["pwdid"]).get()
            data_list = len(likes)
            # cc = 0
            # print(data_list)
            if data_list > 0:
                # cc = cc + 1
                post_data.append({"post":i.to_dict(),"id":i.id,"user":pro,"condition":1,"count":data_list_count})
            else:
                post_data.append({"post":i.to_dict(),"id":i.id,"user":pro,"condition":0,"count":data_list_count})
        return render(request, 'pwd/Homepage.html',{"post":post_data})
    else:
        return redirect("Guest:login")

# profile
def profile(request):
    if "pwdid" in request.session:
        pwd = db.collection("tbl_pwd").document(request.session["pwdid"]).get().to_dict()
        return render(request, 'pwd/MyProfile.html',{"pwd": pwd})
    else:
        return redirect("Guest:login")

# Edit profile
def editprofile(request):
    if "pwdid" in request.session:
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
    else:
        return redirect("Guest:login")

# Change Password
def changepassword(request):
    if "pwdid" in request.session:
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
    else:
        return redirect("Guest:login")

# Request
def viewrequest(request):
    if "pwdid" in request.session:
        requestdata = []
        req = db.collection("tbl_request").where("pwd_id", "==", request.session["pwdid"]).where("request_status", "==", 0).stream()
        for r in req:
            req = r.to_dict()
            user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
            requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
        return render(request,"PWD/View_Request.html",{"request":requestdata})
    else:
        return redirect("Guest:login")

def reply(request, id):
    if "pwdid" in request.session:
        if request.method == "POST":
            req = db.collection("tbl_request").document(id).update({"request_reply":request.POST.get("txt_reply"),"request_status":1})
            return render(request,"Pwd/Reply.html",{"msg":"Reply Send Successfully"})
        else:
            return render(request,"Pwd/Reply.html")
    else:
        return redirect("Guest:login")

def replyedrequest(request):
    if "pwdid" in request.session:
        requestdata = []
        req = db.collection("tbl_request").where("pwd_id", "==", request.session["pwdid"]).where("request_status", "==", 1).stream()
        for r in req:
            req = r.to_dict()
            user = db.collection("tbl_user").document(req["user_id"]).get().to_dict()
            requestdata.append({"data":r.to_dict(),"id":r.id,"user":user})
        return render(request,"PWD/Replyed_Request.html",{"request":requestdata})
    else:
        return redirect("Guest:login")

# Complaint
def complaint(request):
    if "pwdid" in request.session:
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
    else:
        return redirect("Guest:login")

# FeedBack
def feedback(request):
    if "pwdid" in request.session:
        if request.method == "POST":
            db.collection("tbl_feedback").add({"feedback_content":request.POST.get("txt_feedback"),
                                                "feedback_date":datetime.now(),
                                                "user_id":"",
                                                "mvd_id":"",
                                                "kseb_id":"",
                                                "municipality_id":"",
                                                "pwd_id":request.session["pwdid"]})
            return render(request,"PWD/FeedBack.html",{"msg":"Feedback Send Sucessfully"})
        else:
            return render(request,"PWD/FeedBack.html",)
    else:
        return redirect("Guest:login")

# View Post
def ajaxlike(request):
    count = db.collection("tbl_like").where("pwd_id", "==", request.session["pwdid"]).where("post_id", "==", request.GET.get("postid")).stream()
    ct = 0
    for c in count:
        ct = ct + 1
        id = c.id
    # print(ct)
    if ct > 0:
        db.collection("tbl_like").document(id).delete()
        likescount = db.collection("tbl_like").where("post_id", "==", request.GET.get("postid")).get()
        data_list_count = len(likescount)
        # print(data_list_count)
        return JsonResponse({"color":1,"count":data_list_count})
    else:
        db.collection("tbl_like").add({"user_id":"",
                                        "post_id":request.GET.get("postid"),
                                        "kseb_id":"",
                                        "pwd_id":request.session["pwdid"],
                                        "mvd_id":"",
                                        "municipality_id":""})
        likescount = db.collection("tbl_like").where("post_id", "==", request.GET.get("postid")).get()
        data_list_count = len(likescount)
        # print(data_list_count)
        return JsonResponse({"color":0,"count":data_list_count})

def ajaxcomment(request):
    db.collection("tbl_comment").add({"post_id":request.GET.get("postid"),
                                        "user_id":"",
                                        "command_content":request.GET.get("content"),
                                        "kseb_id":"",
                                        "pwd_id":request.session["pwdid"],
                                        "mvd_id":"",
                                        "municipality_id":""})
    comment = db.collection("tbl_comment").where("post_id", "==", request.GET.get("postid")).stream()
    com_data = []
    for c in comment:
        cm = c.to_dict()
        if cm["pwd_id"] != "":
            pwd = db.collection("tbl_pwd").document(cm["pwd_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"pwd":pwd,"photo":"0"})
        elif cm["user_id"] != "":
            user = db.collection("tbl_user").document(cm["user_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"user":user,"photo":"1"})
        elif cm["kseb_id"] != "":
            kseb = db.collection("tbl_kseb").document(cm["kseb_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"kseb":kseb,"photo":"0"})
        elif cm["mvd_id"] != "":
            mvd = db.collection("tbl_mvd").document(cm["mvd_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"mvd":mvd,"photo":"0"})
        elif cm["municipality_id"] != "":
            municipality = db.collection("tbl_municipality").document(cm["municipality_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"municipality":municipality,"photo":"0"})
    return render(request,"PWD/AjaxComment.html",{"comment":com_data})

def ajaxgetcommant(request):
    comment = db.collection("tbl_comment").where("post_id", "==",request.GET.get("postid")).stream()
    com_data = []
    for c in comment:
        cm = c.to_dict()
        if cm["pwd_id"] != "":
            pwd = db.collection("tbl_pwd").document(cm["pwd_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"pwd":pwd,"photo":"0"})
        elif cm["user_id"] != "":
            user = db.collection("tbl_user").document(cm["user_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"user":user,"photo":"1"})
        elif cm["kseb_id"] != "":
            kseb = db.collection("tbl_kseb").document(cm["kseb_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"kseb":kseb,"photo":"0"})
        elif cm["mvd_id"] != "":
            mvd = db.collection("tbl_mvd").document(cm["mvd_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"mvd":mvd,"photo":"0"})
        elif cm["municipality_id"] != "":
            municipality = db.collection("tbl_municipality").document(cm["municipality_id"]).get().to_dict()
            com_data.append({"comment":c.to_dict(),"id":c.id,"municipality":municipality,"photo":"0"})
    return render(request,"PWD/AjaxComment.html",{"comment":com_data})

# Logout
def logout(request):
    del request.session["pwdid"]
    return redirect("Guest:login")