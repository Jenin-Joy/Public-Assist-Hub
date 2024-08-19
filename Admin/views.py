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