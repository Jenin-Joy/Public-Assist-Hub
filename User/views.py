from django.shortcuts import render
import firebase_admin
from firebase_admin import firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
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

# Search PWD
def searchpwd(request):
    district = db.collection("tbl_district").stream()
    districtdata = getData(district)
    return render(request,"User/Search_pwd.html",{"district":districtdata})

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
    district = db.collection("tbl_district").stream()
    districtdata = getData(district)
    return render(request,"User/Search_mvd.html",{'data':districtdata})

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
    district = db.collection("tbl_district").stream()
    districtdata = getData(district)
    return render(request,"User/Search_municipality.html",{'data':districtdata})

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
    district = db.collection("tbl_district").stream()
    districtdata = getData(district)
    return render(request,"User/Search_kseb.html",{"data":districtdata})

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