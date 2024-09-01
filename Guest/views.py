from django.shortcuts import render, redirect
import firebase_admin
from firebase_admin import firestore,auth,storage,credentials
import pyrebase
# Create your views here.

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

# Register municipality
def municipality(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            municipality = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError, ValueError) as error:
            return render(request,"Guest/Municipality.html",{"msg":error})
        image = request.FILES.get("txt_photo")
        if image:
            path = "Municipality/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_municipality").document(municipality.uid).set({"municipality_name":request.POST.get('txt_name'),"municipality_contact":request.POST.get('txt_contact'),"municipality_email":request.POST.get('txt_email'),"municipality_address":request.POST.get('txt_address'),"municipality_password":request.POST.get('txt_password'),"district_id":request.POST.get("sel_district"),"municipality_proof":download_url,"municipality_status":0})
        return render(request,"Guest/Municipality.html",{"msg":"Sucessfully Registred"})
    else:
        return render(request,"Guest/Municipality.html",{"district":district})

# Register user
def user(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    municipalitydata = db.collection("tbl_municipality").stream()
    municipality = getData(municipalitydata)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError, ValueError) as error:
            return render(request,"Guest/User.html",{"msg":error})
        image = request.FILES.get("txt_photo")
        if image:
            path = "User/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_user").document(user.uid).set({"user_name":request.POST.get('txt_name'),"user_contact":request.POST.get('txt_contact'),"user_email":request.POST.get('txt_email'),"user_address":request.POST.get('txt_address'),"user_password":request.POST.get('txt_password'),"municipality_id":request.POST.get("sel_municipality"),"localplace_id":request.POST.get("sel_locplace"),"user_photo":download_url})
        return render(request,"Guest/User.html",{"msg":"Registred Sucessfully"})
    else:
        return render(request,"Guest/User.html",{"district":district,"municipality":municipality})

# Ajax function for municipality
def ajaxmunicipality(request):
    municipalitydata=db.collection("tbl_municipality").where("district_id", "==", request.GET.get('disd')).stream()
    municipality = getData(municipalitydata)
    return render(request,"Guest/Ajaxmunicipality.html",{'data':municipality})

# Ajax function for local place
def ajaxlocalplace(request):
    localplacedata=db.collection("tbl_local_place").where("place_id", "==", request.GET.get('disd')).stream()
    localplace = getData(localplacedata)
    return render(request,"Guest/Ajaxlocalplace.html",{'data':localplace})

# Register pwd
def pwd(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            pwd = firebase_admin.auth.create_user(email=email, password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError, ValueError) as error:
            return render(request,"Guest/pwd.html",{'msg':error})
        image = request.FILES.get("txt_photo")
        if image:
            path = "PWD/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_pwd").document(pwd.uid).set({"pwd_name":request.POST.get('txt_name'),"pwd_contact":request.POST.get('txt_contact'),"pwd_email":request.POST.get('txt_email'),"pwd_address":request.POST.get('txt_address'),"pwd_password":request.POST.get('txt_password'),"district_id":request.POST.get("sel_district"),"pwd_proof":download_url,"pwd_status":0})
        return render(request,"Guest/pwd.html",{'msg':'Registred Sucessfully'})
    else:
        return render(request,"Guest/pwd.html",{'district':district})

# Register mvd
def mvd(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            mvd = firebase_admin.auth.create_user(email=email, password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError, ValueError) as error:
            return render(request,"Guest/mvd.html",{'msg':error})
        image = request.FILES.get("txt_photo")
        if image:
            path = "Mvd/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_mvd").document(mvd.uid).set({"mvd_name":request.POST.get('txt_name'),"mvd_contact":request.POST.get('txt_contact'),"mvd_email":request.POST.get('txt_email'),"mvd_address":request.POST.get('txt_address'),"mvd_password":request.POST.get('txt_password'),"district_id":request.POST.get("sel_district"),"mvd_proof":download_url,"mvd_status":0})
        return render(request,"Guest/mvd.html",{'msg':'Registred Sucessfully'})
    else:
        return render(request,"Guest/mvd.html",{'district':district})

# Registre kseb
def kseb(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            kseb = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError, ValueError) as error:
            return render(request,"Guest/kseb.html",{"msg":error})
        image = request.FILES.get("txt_photo")
        if image:
            path = "Kseb/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        db.collection("tbl_kseb").document(kseb.uid).set({"kseb_name":request.POST.get('txt_name'),"kseb_contact":request.POST.get('txt_contact'),"kseb_email":request.POST.get('txt_email'),"kseb_address":request.POST.get('txt_address'),"kseb_password":request.POST.get('txt_password'),"localplace_id":request.POST.get("sel_locplace"),"kseb_proof":download_url,"kseb_status":0})
        return render(request,"Guest/kseb.html",{"msg":"Registred Sucessfully"})
    else:
        return render(request,"Guest/kseb.html",{"district":district})

# login function
def login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            data = auth.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/login.html",{"msg":"Invalid Email or Password"})
        userdata = db.collection("tbl_user").document(data["localId"]).get().to_dict()
        municipalitydata = db.collection("tbl_municipality").document(data["localId"]).get().to_dict()
        mvddata = db.collection("tbl_mvd").document(data["localId"]).get().to_dict()
        pwddata = db.collection("tbl_pwd").document(data["localId"]).get().to_dict()
        ksebdata = db.collection("tbl_kseb").document(data["localId"]).get().to_dict()
        admindata = db.collection("tbl_admin").document(data["localId"]).get().to_dict()
        if userdata:
            if userdata["user_password"] == password:
                request.session["uid"] = data["localId"]
                return redirect("User:homepage")
            else:
                db.collection("tbl_user").document(data["localId"]).update({"user_password":password})
                return redirect("User:homepage")
        elif municipalitydata:
            if municipalitydata["municipality_status"] == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Verification is Pending"})
            elif municipalitydata["municipality_status"] == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Account is Deactivated"})
            else:
                if municipalitydata["municipality_password"] == password:
                    request.session["mid"] = data["localId"]
                    return redirect("Municipality:homepage")
                else:
                    db.collection("tbl_municipality").document(data["localId"]).update({"municipality_password":password})
                    return redirect("Municipality:homepage")
        elif mvddata:
            if mvddata["mvd_status"] == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Verification is Pending"})
            elif mvddata["mvd_status"] == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Account is Deactivated"})
            else:
                if mvddata["mvd_password"] == password:
                    request.session["mvdid"] = data["localId"]
                    return redirect("MVD:homepage")
                else:
                    db.collection("tbl_mvd").document(data["localId"]).update({"mvd_password":password})
                    return redirect("MVD:homepage")
        elif pwddata:
            if pwddata["pwd_status"] == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Verification is Pending"})
            elif pwddata["pwd_status"] == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Account is Deactivated"})
            else:
                if pwddata["pwd_password"] == password:
                    request.session["pwdid"] = data["localId"]
                    return redirect("PWD:homepage")
                else:
                    db.collection("tbl_pwd").document(data["localId"]).update({"pwd_password":password})
                    return redirect("PWD:homepage")
        elif ksebdata:
            if ksebdata["kseb_status"] == 0:
                return render(request,"Guest/Login.html",{"msg":"Your Verification is Pending"})
            elif ksebdata["kseb_status"] == 2:
                return render(request,"Guest/Login.html",{"msg":"Your Account is Deactivated"})
            else:
                if ksebdata["kseb_password"] == password:
                    request.session["ksebid"] = data["localId"]
                    return redirect("KSEB:homepage")
                else:
                    db.collection("tbl_kseb").document(data["localId"]).update({"kseb_password":password})
                    return redirect("KSEB:homepage")
        elif admindata:
            request.session["aid"] = data["localId"]
            return redirect("Admin:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Error"})
    else:
        return render(request,"Guest/Login.html")