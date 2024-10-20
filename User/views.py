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

# Data Base connection
db = firestore.client()

config = {
  "apiKey": "AIzaSyCOZFTE8q_uo15903C2s0mbMGtqEg22nL8",
  "authDomain": "public-assist-hub.firebaseapp.com",
  "projectId": "public-assist-hub",
  "storageBucket": "public-assist-hub.appspot.com",
  "messagingSenderId": "49732244996",
  "appId": "1:49732244996:web:e37b617ce5b4c1dc0d8751",
  "measurementId": "G-BK2V8RG2JJ",
  "databaseURL":""
}

# App config using pyrebase
firebase = pyrebase.initialize_app(config)

# Authication for login
auth = firebase.auth()

# for file upload
sd = firebase.storage()

# convert data into dictionary
def getData(data):
    datas = []
    for i in data:
        datas.append({"data":i.to_dict(),"id":i.id})
    return datas

# Home Page Function
def homepage(request):
    if "uid" in request.session:
        post = db.collection("tbl_post").stream()
        post_data = []
        for i in post:
            likescount = db.collection("tbl_like").where("post_id", "==", i.id).get()
            data_list_count = len(likescount)
            # print(data_list_count)
            ps = i.to_dict()
            pro = db.collection("tbl_user").document(ps["user_id"]).get().to_dict()
            likes = db.collection("tbl_like").where("post_id", "==", i.id).where("user_id", "==", request.session["uid"]).get()
            data_list = len(likes)
            # cc = 0
            # print(data_list)
            if data_list > 0:
                # cc = cc + 1
                post_data.append({"post":i.to_dict(),"id":i.id,"user":pro,"condition":1,"count":data_list_count})
            else:
                post_data.append({"post":i.to_dict(),"id":i.id,"user":pro,"condition":0,"count":data_list_count})
        return render(request, 'User/Homepage.html',{"post":post_data})
    else:
        return redirect("Guest:login")

# profile
def profile(request):
    if "uid" in request.session:
        user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        return render(request, 'User/MyProfile.html',{"user": user})
    else:
        return redirect("Guest:login")

# Edit profile
def editprofile(request):
    if "uid" in request.session:
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
    else:
        return redirect("Guest:login")

# Change Password
def changepassword(request):
    if "uid" in request.session:
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
    else:
        return redirect("Guest:login")

# Search PWD
def searchpwd(request):
    if "uid" in request.session:
        district = db.collection("tbl_district").stream()
        districtdata = getData(district)
        return render(request,"User/Search_pwd.html",{"district":districtdata})
    else:
        return redirect("Guest:login")

def ajaxsearchpwd(request):
    if request.GET.get("district"):
        pwd = db.collection("tbl_pwd").where("district_id", "==", request.GET.get("district")).stream()
        pwddata = getData(pwd)
        return render(request,"User/Ajaxsearchpwd.html",{'data':pwddata})
    else:
        pwd = db.collection("tbl_pwd").stream()
        pwddata = getData(pwd)
        return render(request,"User/Ajaxsearchpwd.html",{'data':pwddata})

# Search MVD
def searchmvd(request):
    if "uid" in request.session:
        district = db.collection("tbl_district").stream()
        districtdata = getData(district)
        return render(request,"User/Search_mvd.html",{'data':districtdata})
    else:
        return redirect("Guest:login")

def ajaxsearchmvd(request): 
    if request.GET.get("district"):
        mvd = db.collection("tbl_mvd").where("district_id", "==", request.GET.get("district")).stream()
        mvddata = getData(mvd)
        return render(request,"User/Ajaxsearchmvd.html",{'data':mvddata})
    else:
        mvd = db.collection("tbl_mvd").stream()
        mvddata = getData(mvd)
        return render(request,"User/Ajaxsearchmvd.html",{"data":mvddata})

# Search Municipality
def searchmunicipality(request):
    if "uid" in request.session:
        district = db.collection("tbl_district").stream()
        districtdata = getData(district)
        return render(request,"User/Search_municipality.html",{'data':districtdata})
    else:
        return redirect("Guest:login")

def ajaxsearchmunicipality(request): 
    if request.GET.get("district"):
        municipality = db.collection("tbl_municipality").where("district_id", "==", request.GET.get("district")).stream()
        municipalitydata = getData(municipality)
        return render(request,"User/Ajaxsearchmunicipality.html",{'data':municipalitydata})
    else:
        municipality = db.collection("tbl_municipality").stream()
        municipalitydata = getData(municipality)
        return render(request,"User/Ajaxsearchmunicipality.html",{"data":municipalitydata})

# Search Kseb
def searchKseb(request):
    if "uid" in request.session:
        district = db.collection("tbl_district").stream()
        districtdata = getData(district)
        return render(request,"User/Search_kseb.html",{"data":districtdata})
    else:
        return redirect("Guest:login")

def ajaxsearchkseb(request):
    ksebdata = []
    if request.GET.get("localplace"):
        kseb = db.collection("tbl_kseb").where("localplace_id", "==", request.GET.get("localplace")).stream()
        ksebdata = getData(kseb)
        return render(request,"User/Ajaxsearchkseb.html",{'data':ksebdata})
    elif request.GET.get("place"):
        localplace = db.collection("tbl_local_place").where("place_id", "==", request.GET.get("place")).stream()
        for p in localplace:
            kseb = db.collection("tbl_kseb").where("localplace_id", "==", p.id).stream()
            for k in kseb:
                ksebdata.append({"data":k.to_dict(),"id":k.id})
        return render(request,"User/Ajaxsearchkseb.html",{'data':ksebdata})
    elif request.GET.get("district"):
        place = db.collection("tbl_place").where("district_id", "==", request.GET.get("district")).stream()
        for p in place:
            localplace = db.collection("tbl_local_place").where("place_id", "==", p.id).stream()
            for pl in localplace:
                kseb = db.collection("tbl_kseb").where("localplace_id", "==", pl.id).stream()
                for k in kseb:
                    ksebdata.append({"data":k.to_dict(),"id":k.id})
        return render(request,"User/Ajaxsearchkseb.html",{'data':ksebdata})
    else:
        kseb = db.collection("tbl_kseb").stream()
        ksebdata = getData(kseb)
        return render(request,"User/Ajaxsearchkseb.html",{"data":ksebdata})

# Mvd Request
def mvdrequest(request, id):
    if "uid" in request.session:
        if request.method == "POST":
            photo = request.FILES.get("txt_photo")
            if photo:
                path = "MvdRequest/" + photo.name
                sd.child(path).put(photo)
                download_url = sd.child(path).get_url(None)
            db.collection("tbl_request").add({"request_date":datetime.now(),
                                            "request_photo":download_url,
                                            "request_description":request.POST.get("txt_description"),
                                            "user_id":request.session["uid"],
                                            "mvd_id":id,
                                            "request_reply":"",
                                            "request_status":0,
                                            "pwd_id":"",
                                            "municipality_id":"",
                                            "kseb_id":""})
            return render(request,"User/Mvd_Request.html",{"msg":"Request Sended Sucessfully"})
        else:
            return render(request,"User/Mvd_Request.html",)
    else:
        return redirect("Guest:login")

# Pwd Request
def pwdrequest(request, id):
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "PwdRequest/" + photo.name
            sd.child(path).put(photo)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_request").add({"request_date":datetime.now(),
                                        "request_photo":download_url,
                                        "request_description":request.POST.get("txt_description"),
                                        "user_id":request.session["uid"],
                                        "mvd_id":"",
                                        "request_reply":"",
                                        "request_status":0,
                                        "pwd_id":id,
                                        "municipality_id":"",
                                        "kseb_id":""})
        return render(request,"User/Pwd_Request.html",{"msg":"Request Sended Sucessfully"})
    else:
        return render(request,"User/Pwd_Request.html",)

# Municipality Request
def municipalityrequest(request, id):
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "MunicipalityRequest/" + photo.name
            sd.child(path).put(photo)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_request").add({"request_date":datetime.now(),
                                        "request_photo":download_url,
                                        "request_description":request.POST.get("txt_description"),
                                        "user_id":request.session["uid"],
                                        "mvd_id":"",
                                        "request_reply":"",
                                        "request_status":0,
                                        "pwd_id":"",
                                        "municipality_id":id,
                                        "kseb_id":""})
        return render(request,"User/Municipality_Request.html",{"msg":"Request Sended Sucessfully"})
    else:
        return render(request,"User/Municipality_Request.html",)

# Kseb Request
def ksebrequest(request, id):
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "KsebRequest/" + photo.name
            sd.child(path).put(photo)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_request").add({"request_date":datetime.now(),
                                        "request_photo":download_url,
                                        "request_description":request.POST.get("txt_description"),
                                        "user_id":request.session["uid"],
                                        "mvd_id":"",
                                        "request_reply":"",
                                        "request_status":0,
                                        "pwd_id":"",
                                        "municipality_id":"",
                                        "kseb_id":id})
        return render(request,"User/Kseb_Request.html",{"msg":"Request Sended Sucessfully"})
    else:
        return render(request,"User/Kseb_Request.html",)

# My Request
def myrequest(request):
    if "uid" in request.session:
        mvdrequestdata =[]
        pwdrequestdata = []
        municipalityrequestdata = []
        ksebrequestdata = []
        mvdrequest = db.collection("tbl_request").where("user_id", "==", request.session["uid"]).where("mvd_id", "!=", "").stream()
        pwdrequest = db.collection("tbl_request").where("user_id", "==", request.session["uid"]).where("pwd_id", "!=", "").stream()
        municipalityrequest = db.collection("tbl_request").where("user_id", "==", request.session["uid"]).where("municipality_id", "!=", "").stream()
        ksebrequest = db.collection("tbl_request").where("user_id", "==", request.session["uid"]).where("kseb_id", "!=", "").stream()
        for m in mvdrequest:
            mvd = m.to_dict()
            mvddata = db.collection("tbl_mvd").document(mvd["mvd_id"]).get().to_dict()
            mvdrequestdata.append({"data":m.to_dict(),"id":m.id,"mvd":mvddata})
        for p in pwdrequest:
            pwd = p.to_dict()
            pwddata = db.collection("tbl_pwd").document(pwd["pwd_id"]).get().to_dict()
            pwdrequestdata.append({"data":p.to_dict(),"id":p.id,"pwd":pwddata})
        for mu in municipalityrequest:
            municipality = mu.to_dict()
            municipalitydata = db.collection("tbl_municipality").document(municipality["municipality_id"]).get().to_dict()
            municipalityrequestdata.append({"data":mu.to_dict(),"id":mu.id,"municipality":municipalitydata})
        for k in ksebrequest:
            kseb = k.to_dict()
            ksebdata = db.collection("tbl_kseb").document(kseb["kseb_id"]).get().to_dict()
            ksebrequestdata.append({"data":k.to_dict(),"id":k.id,"kseb":ksebdata})
        return render(request,"User/My_Request.html",{"mvdrequest":mvdrequestdata, "pwdrequest":pwdrequestdata, "municipalityrequest":municipalityrequestdata, "ksebrequest":ksebrequestdata})
    else:
        return redirect("Guest:login")

# Complaint
def complaint(request):
    if "uid" in request.session:
        complaint = db.collection("tbl_complaint").where("user_id", "==", request.session["uid"]).stream()
        complaintdata = getData(complaint)
        if request.method == "POST":
            db.collection("tbl_complaint").add({"complaint_title":request.POST.get("txt_title"),
                                                "complaint_content":request.POST.get("txt_content"),
                                                "complaint_date":datetime.now(),
                                                "complaint_reply":"",
                                                "complaint_status":0,
                                                "complaint_photo":"",
                                                "user_id":request.session["uid"],
                                                "municipality_id":"",
                                                "kseb_id":"",
                                                "pwd_id":"",
                                                "mvd_id":""})
            return render(request,"User/Complaint.html",{"msg":"Complaint Send Sucessfully"})
        else:
            return render(request,"User/Complaint.html",{"complaint":complaintdata})
    else:
        return redirect("Guest:login")

# Offical Complaint Municipality
def OfficalComplaintMunicipality(request, id):
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "OfficialComplaint/" + photo.name
            sd.child(path).put(photo)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_complaint").add({"complaint_title":request.POST.get("txt_title"),
                                            "complaint_content":request.POST.get("txt_content"),
                                            "complaint_photo":download_url,
                                            "complaint_date":datetime.now(),
                                            "complaint_status":0,
                                            "complaint_reply":"",
                                            "user_id":request.session["uid"],
                                            "municipality_id":id,
                                            "kseb_id":"",
                                            "pwd_id":"",
                                            "mvd_id":""})   
        return render(request,"User/OfficialsComplaint.html",{"msg":"Complaint Send Sucessfully"})
    else:
        return render(request,"User/OfficialsComplaint.html",)

# Offical Complaint MVD
def OfficalComplaintMvd(request, id):
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "OfficialComplaint/" + photo.name
            sd.child(path).put(photo)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_complaint").add({"complaint_title":request.POST.get("txt_title"),
                                            "complaint_content":request.POST.get("txt_content"),
                                            "complaint_photo":download_url,
                                            "complaint_date":datetime.now(),
                                            "complaint_status":0,
                                            "complaint_reply":"",
                                            "user_id":request.session["uid"],
                                            "municipality_id":"",
                                            "kseb_id":"",
                                            "pwd_id":"",
                                            "mvd_id":id})   
        return render(request,"User/OfficialsComplaint.html",{"msg":"Complaint Send Sucessfully"})
    else:
        return render(request,"User/OfficialsComplaint.html",)

# View Offical Complaint
def viewofficialcomplaints(request):
    if "uid" in request.session:
        municipality = db.collection("tbl_complaint").where("user_id", "==", request.session["uid"]).where("municipality_id", "!=", "").stream()
        mvd = db.collection("tbl_complaint").where("user_id", "==", request.session["uid"]).where("mvd_id", "!=", "").stream()
        munidata = []
        mvddata = []
        for i in municipality:
            com = i.to_dict()
            muni = db.collection("tbl_municipality").document(com["municipality_id"]).get().to_dict()
            munidata.append({"data":com, "id":i.id, "municipality":muni})
        for i in mvd:
            com = i.to_dict()
            mv = db.collection("tbl_mvd").document(com["mvd_id"]).get().to_dict()
            mvddata.append({"data":com, "id":i.id, "mvd":mv})
        return render(request,"User/ViewOfficalComplaint.html",{"mvdcomplaint":mvddata,"municipalitycomplaint":munidata})
    else:
        return redirect("Guest:login")

# Add Post
def addpost(request):
    if "uid" in request.session:
        posts = db.collection("tbl_post").where("user_id", "==", request.session["uid"]).stream()
        postdata = getData(posts)
        if request.method == "POST":
            photo = request.FILES.get("txt_photo")
            if photo:
                path = "Post/" + photo.name
                sd.child(path).put(photo)
                download_url = sd.child(path).get_url(None)
            db.collection("tbl_post").add({"post_caption":request.POST.get("txt_caption"),
                                            "post_description":request.POST.get("txt_description"),
                                            "post_photo":download_url,
                                            "post_date":datetime.now(),
                                            "user_id":request.session["uid"]})
            return render(request,"User/AddPost.html",{"msg":"Post Added Sucessfully"})
        else:
            return render(request,"User/AddPost.html",{"post":postdata})
    else:
        return redirect("Guest:login")

# Delete Post
def deletepost(request, id):
    db.collection("tbl_post").document(id).delete()
    return render(request,"User/AddPost.html",{"msg":"Post Deleted"})

# View Post
def ajaxlike(request):
    if "uid" in request.session:
        count = db.collection("tbl_like").where("user_id", "==", request.session["uid"]).where("post_id", "==", request.GET.get("postid")).stream()
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
            db.collection("tbl_like").add({"user_id":request.session["uid"],
                                            "post_id":request.GET.get("postid"),
                                            "kseb_id":"",
                                            "pwd_id":"",
                                            "mvd_id":"",
                                            "municipality_id":""})
            likescount = db.collection("tbl_like").where("post_id", "==", request.GET.get("postid")).get()
            data_list_count = len(likescount)
            # print(data_list_count)
            return JsonResponse({"color":0,"count":data_list_count})
    else:
        return redirect("Guest:login")

def ajaxcomment(request):
    db.collection("tbl_comment").add({"post_id":request.GET.get("postid"),
                                        "user_id":request.session["uid"],
                                        "command_content":request.GET.get("content"),
                                        "kseb_id":"",
                                        "pwd_id":"",
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
    return render(request,"User/AjaxComment.html",{"comment":com_data})

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
    return render(request,"User/AjaxComment.html",{"comment":com_data})

# FeedBack
def feedback(request):
    if "uid" in request.session:
        if request.method == "POST":
            db.collection("tbl_feedback").add({"feedback_content":request.POST.get("txt_feedback"),
                                                "feedback_date":datetime.now(),
                                                "user_id":request.session["uid"],
                                                "mvd_id":"",
                                                "kseb_id":"",
                                                "municipality_id":"",
                                                "pwd_id":""})
            return render(request,"User/FeedBack.html",{"msg":"Feedback Send Sucessfully"})
        else:
            return render(request,"User/FeedBack.html",)
    else:
        return redirect("Guest:login")

# Logout
def logout(request):
    del request.session["uid"]
    return redirect("Guest:login")