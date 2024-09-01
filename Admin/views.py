from django.shortcuts import render,redirect
from Admin.models import *
import firebase_admin
from firebase_admin import credentials,auth,storage,firestore
import pyrebase
# Create your views here.

db = firestore.client()

# convert data into dictionary
def getData(data):
    datas = []
    for i in data:
        datas.append({"data":i.to_dict(),"id":i.id})
    return datas

# Homepage function
def homepage(request):
    return render(request, 'Admin/Homepage.html')

# district insert and select function
def district(request):
    districtdata = db.collection("tbl_district").stream()
    district = getData(districtdata)
    # print(district)
    if request.method=="POST":
        db.collection("tbl_district").add({"district_name":request.POST.get("txt_district")})
        return render(request,"Admin/District.html",{'msg':"Data Inserted"})
    else:
        return render(request,"Admin/District.html",{"district":district})

# district delete function
def deletedistrict(request,did):
    db.collection("tbl_district").document(did).delete()
    return render(request,"Admin/District.html",{'msg':"Data Deleted"})

# district edit function
def editdistrict(request,eid):
    data=db.collection("tbl_district").document(eid).get().to_dict() 
    if request.method=="POST":
        db.collection("tbl_district").document(eid).update({"district_name":request.POST.get("txt_district")})
        return render(request,"Admin/District.html",{'msg':"Data Updated"})
    else:
        return render(request,"Admin/District.html",{'editdis':data})

# place insert and select function
def place(request):
    districtdata=db.collection("tbl_district").stream()
    district = getData(districtdata)
    placedata=db.collection("tbl_place").stream()
    place = []
    for i in placedata:
        placedis = i.to_dict()
        place.append({"place":i.to_dict(),"id":i.id,"district":db.collection("tbl_district").document(placedis["district_id"]).get().to_dict()})
    if request.method=="POST":
        db.collection("tbl_place").add({"place_name":request.POST.get("txt_place"),"district_id":request.POST.get('sel_district')})
        return render(request,"Admin/Place.html",{'msg':"Data Inserted"})
    else:
        return render(request,"Admin/Place.html",{'district':district,"place":place})

# place edit function
def editplace(request,pid):
    districtdata=db.collection("tbl_district").stream()
    district = getData(districtdata)
    data=db.collection("tbl_place").document(pid).get().to_dict()
    if request.method=="POST":
        db.collection("tbl_place").document(pid).update({"place_name":request.POST.get("txt_place"),"district_id":request.POST.get('sel_district')})
        return render(request,"Admin/Place.html",{'msg':"Data Updated"})
    else:
        return render(request,"Admin/Place.html",{'district':district,'data':data})

# place delete function
def deleteplace(request,pid):
    db.collection("tbl_place").document(pid).delete()
    return render(request,"Admin/Place.html",{'msg':"Data Deleted"})

# local place insert and select
def localplace(request):
    districtdata=db.collection("tbl_district").stream()
    district = getData(districtdata)
    localdata = db.collection("tbl_local_place").stream()
    localplace = []
    for i in localdata:
        localdis = i.to_dict()
        place = db.collection("tbl_place").document(localdis["place_id"]).get().to_dict()
        localplace.append({"localplace":i.to_dict(),"id":i.id,"place":place,"district":db.collection("tbl_district").document(place["district_id"]).get().to_dict()})
    if request.method=="POST":
        db.collection("tbl_local_place").add({"localplace_name":request.POST.get("txt_localplace"),"place_id":request.POST.get('sel_place')})
        return render(request,"Admin/Local_place.html",{'msg':"Data Inserted"})
    else:
        return render(request,"Admin/Local_place.html",{'district':district,"localplace":localplace})

# local place delete function
def deletelocplace(request,locid):
    db.collection("tbl_local_place").document(locid).delete()
    return render(request,"Admin/Local_place.html",{'msg':"Data Deleted"})

# ajax function for place
def ajaxplace(request):
    placedata=db.collection("tbl_place").where("district_id", "==", request.GET.get('disd')).stream()
    place = getData(placedata)
    return render(request,"Admin/Ajaxplace.html",{'data':place})

# admin registration and select function
def adminreg(request):
    admindata = db.collection("tbl_admin").stream()
    admin = getData(admindata)
    if request.method=="POST":
        email = request.POST.get('txt_email')
        password = request.POST.get('txt_password')
        try:
            admin = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Admin/Admin_Registration.html",{'msg':error})

        db.collection("tbl_admin").document(admin.uid).set({"admin_name":request.POST.get('txt_name'),"admin_email":request.POST.get('txt_email'),"admin_password":request.POST.get('txt_password')})
        return render(request,"Admin/Admin_Registration.html",{'msg':"Data Inserted"})
    else:
        return render(request,"Admin/Admin_Registration.html",{"data":admin})

# admin delete function
def deleteadmin(request,did):
    firebase_admin.auth.delete_user(did)
    db.collection("tbl_admin").document(did).delete()
    return render(request,"Admin/Admin_Registration.html",{'msg':"Data Deleted"})

# New Municipality
def newmunicipality(request):
    municipality = db.collection("tbl_municipality").where("municipality_status", "==", 0).stream()
    municipality_data = []
    for i in municipality:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/New_Municipality.html",{"municipality":municipality_data})

# Municipality Verification
def municipalityverification(request,id,status):
    municipality = db.collection("tbl_municipality").document(id).update({"municipality_status":status})
    msg = ""
    if status == 1:
        msg = "Municipality Approved"
    else:
        msg = "Municipality Declined"
    return render(request,"Admin/Homepage.html", {"msg":msg})

# Approved Municipality
def approvedmunicipality(request):
    municipality = db.collection("tbl_municipality").where("municipality_status", "==", 1).stream()
    municipality_data = []
    for i in municipality:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Approved_Municipality.html",{"municipality":municipality_data})

# Rejected Municipality
def rejectedmunicipality(request):
    municipality = db.collection("tbl_municipality").where("municipality_status", "==", 2).stream()
    municipality_data = []
    for i in municipality:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Rejected_Municipality.html",{"municipality":municipality_data})

# New Kseb
def newkseb(request):
    Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 0).stream()
    Kseb_data = []
    for i in Kseb:
        mun = i.to_dict()
        localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
        place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
        district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
        Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
    return render(request,"Admin/New_Kseb.html",{"kseb":Kseb_data})

# Kseb Verification
def ksebverification(request,id,status):
    Kseb = db.collection("tbl_kseb").document(id).update({"kseb_status":status})
    msg = ""
    if status == 1:
        msg = "Kseb Approved"
    else:
        msg = "Kseb Declined"
    return render(request,"Admin/Homepage.html", {"msg":msg})

# Approved Kseb
def approvedkseb(request):
    Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 1).stream()
    Kseb_data = []
    for i in Kseb:
        mun = i.to_dict()
        localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
        place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
        district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
        Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
    return render(request,"Admin/Approved_Kseb.html",{"kseb":Kseb_data})

# Rejected Kseb
def rejectedkseb(request):
    Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 2).stream()
    Kseb_data = []
    for i in Kseb:
        mun = i.to_dict()
        localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
        place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
        district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
        Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
    return render(request,"Admin/Rejected_Kseb.html",{"kseb":Kseb_data})

# New Mvd
def newmvd(request):
    mvd = db.collection("tbl_mvd").where("mvd_status", "==", 0).stream()
    mvd_data = []
    for i in mvd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/New_Mvd.html",{"mvd":mvd_data})

# Mvd Verification
def mvdverification(request,id,status):
    mvd = db.collection("tbl_mvd").document(id).update({"mvd_status":status})
    msg = ""
    if status == 1:
        msg = "Mvd Approved"
    else:
        msg = "Mvd Declined"
    return render(request,"Admin/Homepage.html", {"msg":msg})

# Approved Mvd
def approvedmvd(request):
    mvd = db.collection("tbl_mvd").where("mvd_status", "==", 1).stream()
    mvd_data = []
    for i in mvd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Approved_Mvd.html",{"mvd":mvd_data})

# Rejected Mvd
def rejectedmvd(request):
    mvd = db.collection("tbl_mvd").where("mvd_status", "==", 2).stream()
    mvd_data = []
    for i in mvd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Rejected_Mvd.html",{"mvd":mvd_data})

# New Pwd
def newpwd(request):
    pwd = db.collection("tbl_pwd").where("pwd_status", "==", 0).stream()
    pwd_data = []
    for i in pwd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/New_Pwd.html",{"pwd":pwd_data})

# Pwd Verification
def pwdverification(request,id,status):
    pwd = db.collection("tbl_pwd").document(id).update({"pwd_status":status})
    msg = ""
    if status == 1:
        msg = "Pwd Approved"
    else:
        msg = "Pwd Declined"
    return render(request,"Admin/Homepage.html", {"msg":msg})

# Approved Pwd
def approvedpwd(request):
    pwd = db.collection("tbl_pwd").where("pwd_status", "==", 1).stream()
    pwd_data = []
    for i in pwd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Approved_Pwd.html",{"pwd":pwd_data})

# Rejected Pwd
def rejectedpwd(request):
    pwd = db.collection("tbl_pwd").where("pwd_status", "==", 2).stream()
    pwd_data = []
    for i in pwd:
        mun = i.to_dict()
        district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
        pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
    return render(request,"Admin/Rejected_Pwd.html",{"pwd":pwd_data})