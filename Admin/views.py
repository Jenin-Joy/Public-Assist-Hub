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
    if "aid" in request.session:
        municipality = db.collection("tbl_municipality").where("municipality_status", "==", 1).stream()
        municipalitycount = len(getData(municipality))
        Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 1).stream()
        Ksebcount = len(getData(Kseb))
        mvd = db.collection("tbl_mvd").where("mvd_status", "==", 1).stream()
        mvdcount = len(getData(mvd))
        pwd = db.collection("tbl_pwd").where("pwd_status", "==", 1).stream()
        pwdcount = len(getData(pwd))
        return render(request, 'Admin/Homepage.html',{"municipality":municipalitycount, "mvd":mvdcount, "pwd":pwdcount, "kseb":Ksebcount})
    else:
        return redirect("Guest:login")

# district insert and select function
def district(request):
    if "aid" in request.session:
        districtdata = db.collection("tbl_district").stream()
        district = getData(districtdata)
        # print(district)
        if request.method=="POST":
            db.collection("tbl_district").add({"district_name":request.POST.get("txt_district")})
            return render(request,"Admin/District.html",{'msg':"Data Inserted"})
        else:
            return render(request,"Admin/District.html",{"district":district})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
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
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
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
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
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
    else:
        return redirect("Guest:login")

# admin delete function
def deleteadmin(request,did):
    firebase_admin.auth.delete_user(did)
    db.collection("tbl_admin").document(did).delete()
    return render(request,"Admin/Admin_Registration.html",{'msg':"Data Deleted"})

# New Municipality
def newmunicipality(request):
    if "aid" in request.session:
        municipality = db.collection("tbl_municipality").where("municipality_status", "==", 0).stream()
        municipality_data = []
        for i in municipality:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/New_Municipality.html",{"municipality":municipality_data})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        municipality = db.collection("tbl_municipality").where("municipality_status", "==", 1).stream()
        municipality_data = []
        for i in municipality:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Approved_Municipality.html",{"municipality":municipality_data})
    else:
        return redirect("Guest:login")

# Rejected Municipality
def rejectedmunicipality(request):
    if "aid" in request.session:
        municipality = db.collection("tbl_municipality").where("municipality_status", "==", 2).stream()
        municipality_data = []
        for i in municipality:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            municipality_data.append({"municipality":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Rejected_Municipality.html",{"municipality":municipality_data})
    else:
        return redirect("Guest:login")

# New Kseb
def newkseb(request):
    if "aid" in request.session:
        Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 0).stream()
        Kseb_data = []
        for i in Kseb:
            mun = i.to_dict()
            localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
            place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
        return render(request,"Admin/New_Kseb.html",{"kseb":Kseb_data})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 1).stream()
        Kseb_data = []
        for i in Kseb:
            mun = i.to_dict()
            localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
            place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
        return render(request,"Admin/Approved_Kseb.html",{"kseb":Kseb_data})
    else:
        return redirect("Guest:login")

# Rejected Kseb
def rejectedkseb(request):
    if "aid" in request.session:
        Kseb = db.collection("tbl_kseb").where("kseb_status", "==", 2).stream()
        Kseb_data = []
        for i in Kseb:
            mun = i.to_dict()
            localplace = db.collection("tbl_local_place").document(mun["localplace_id"]).get().to_dict()
            place = db.collection("tbl_place").document(localplace["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            Kseb_data.append({"kseb":i.to_dict(), "district":district,"place":place,"localplace":localplace,"id":i.id})
        return render(request,"Admin/Rejected_Kseb.html",{"kseb":Kseb_data})
    else:
        return redirect("Guest:login")

# New Mvd
def newmvd(request):
    if "aid" in request.session:
        mvd = db.collection("tbl_mvd").where("mvd_status", "==", 0).stream()
        mvd_data = []
        for i in mvd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/New_Mvd.html",{"mvd":mvd_data})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        mvd = db.collection("tbl_mvd").where("mvd_status", "==", 1).stream()
        mvd_data = []
        for i in mvd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Approved_Mvd.html",{"mvd":mvd_data})
    else:
        return redirect("Guest:login")

# Rejected Mvd
def rejectedmvd(request):
    if "aid" in request.session:
        mvd = db.collection("tbl_mvd").where("mvd_status", "==", 2).stream()
        mvd_data = []
        for i in mvd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            mvd_data.append({"mvd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Rejected_Mvd.html",{"mvd":mvd_data})
    else:
        return redirect("Guest:login")

# New Pwd
def newpwd(request):
    if "aid" in request.session:
        pwd = db.collection("tbl_pwd").where("pwd_status", "==", 0).stream()
        pwd_data = []
        for i in pwd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/New_Pwd.html",{"pwd":pwd_data})
    else:
        return redirect("Guest:login")

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
    if "aid" in request.session:
        pwd = db.collection("tbl_pwd").where("pwd_status", "==", 1).stream()
        pwd_data = []
        for i in pwd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Approved_Pwd.html",{"pwd":pwd_data})
    else:
        return redirect("Guest:login")

# Rejected Pwd
def rejectedpwd(request):
    if "aid" in request.session:
        pwd = db.collection("tbl_pwd").where("pwd_status", "==", 2).stream()
        pwd_data = []
        for i in pwd:
            mun = i.to_dict()
            district = db.collection("tbl_district").document(mun["district_id"]).get().to_dict()
            pwd_data.append({"pwd":i.to_dict(), "district":district,"id":i.id})
        return render(request,"Admin/Rejected_Pwd.html",{"pwd":pwd_data})
    else:
        return redirect("Guest:login")

# Complaint
def complaint(request):
    if "aid" in request.session:
        userdata = []
        pwddata = []
        ksebdata = []
        municipalitydata = []
        mvddata = []
        user = db.collection("tbl_complaint").where("user_id", "!=", "").where("complaint_status", "==", 0).stream()
        for u in user:
            us = u.to_dict()
            userdetails = db.collection("tbl_user").document(us["user_id"]).get().to_dict()
            userdata.append({"data":u.to_dict(),"id":u.id,"user":userdetails})
        pwd = db.collection("tbl_complaint").where("pwd_id", "!=", "").where("complaint_status", "==", 0).stream()
        for p in pwd:
            pw = p.to_dict()
            pwddetails = db.collection("tbl_pwd").document(pw["pwd_id"]).get().to_dict()
            pwddata.append({"data":p.to_dict(),"id":p.id,"pwd":pwddetails})
        mvd = db.collection("tbl_complaint").where("mvd_id", "!=", "").where("complaint_status", "==", 0).stream()
        for m in mvd:
            mv = m.to_dict()
            mvddetails = db.collection("tbl_mvd").document(mv["mvd_id"]).get().to_dict()
            mvddata.append({"data":m.to_dict(),"id":m.id,"mvd":mvddetails})
        kseb = db.collection("tbl_complaint").where("kseb_id", "!=", "").where("complaint_status", "==", 0).stream()
        for k in kseb:
            ks = k.to_dict()
            ksebdetails = db.collection("tbl_kseb").document(ks["kseb_id"]).get().to_dict()
            ksebdata.append({"data":k.to_dict(),"id":k.id,"kseb":ksebdetails})
        municipality = db.collection("tbl_complaint").where("municipality_id", "!=", "").where("complaint_status", "==", 0).stream()
        for m in municipality:
            mu = m.to_dict()
            municipalitydetails = db.collection("tbl_municipality").document(mu["municipality_id"]).get().to_dict()
            municipalitydata.append({"data":m.to_dict(),"id":m.id,"municipality":municipalitydetails})
        return render(request,"Admin/View_Complaint.html",{"user":userdata,"pwd":pwddata,"kseb":ksebdata,"municipality":municipalitydata,"mvd":mvddata})
    else:
        return redirect("Guest:login")

# Reply
def reply(request, id):
    if request.method == "POST":
        db.collection("tbl_complaint").document(id).update({"complaint_reply":request.POST.get("txt_reply"),"complaint_status":1})
        return render(request,"Admin/Reply.html",{"msg":"Reply Sended Successfully"})
    else:
        return render(request,"Admin/Reply.html")

# Replyed Complaint
def replyedcomplaint(request):
    if "aid" in request.session:
        userdata = []
        pwddata = []
        ksebdata = []
        municipalitydata = []
        mvddata = []
        user = db.collection("tbl_complaint").where("user_id", "!=", "").where("complaint_status", "==", 1).stream()
        for u in user:
            us = u.to_dict()
            userdetails = db.collection("tbl_user").document(us["user_id"]).get().to_dict()
            userdata.append({"data":u.to_dict(),"id":u.id,"user":userdetails})
        pwd = db.collection("tbl_complaint").where("pwd_id", "!=", "").where("complaint_status", "==", 1).stream()
        for p in pwd:
            pw = p.to_dict()
            pwddetails = db.collection("tbl_pwd").document(pw["pwd_id"]).get().to_dict()
            pwddata.append({"data":p.to_dict(),"id":p.id,"pwd":pwddetails})
        mvd = db.collection("tbl_complaint").where("mvd_id", "!=", "").where("complaint_status", "==", 1).stream()
        for m in mvd:
            mv = m.to_dict()
            mvddetails = db.collection("tbl_mvd").document(mv["mvd_id"]).get().to_dict()
            mvddata.append({"data":m.to_dict(),"id":m.id,"mvd":mvddetails})
        kseb = db.collection("tbl_complaint").where("kseb_id", "!=", "").where("complaint_status", "==", 1).stream()
        for k in kseb:
            ks = k.to_dict()
            ksebdetails = db.collection("tbl_kseb").document(ks["kseb_id"]).get().to_dict()
            ksebdata.append({"data":k.to_dict(),"id":k.id,"kseb":ksebdetails})
        municipality = db.collection("tbl_complaint").where("municipality_id", "!=", "").where("complaint_status", "==", 1).stream()
        for m in municipality:
            mu = m.to_dict()
            municipalitydetails = db.collection("tbl_municipality").document(mu["municipality_id"]).get().to_dict()
            municipalitydata.append({"data":m.to_dict(),"id":m.id,"municipality":municipalitydetails})
        return render(request,"Admin/Replyed_Complaint.html",{"user":userdata,"pwd":pwddata,"kseb":ksebdata,"municipality":municipalitydata,"mvd":mvddata})
    else:
        return redirect("Guest:login")

# FeedBack
def viewfeedback(request):
    if "aid" in request.session:
        userdata = []
        pwddata = []
        ksebdata = []
        municipalitydata = []
        mvddata = []
        user = db.collection("tbl_feedback").where("user_id", "!=", "").stream()
        for u in user:
            us = u.to_dict()
            userdetails = db.collection("tbl_user").document(us["user_id"]).get().to_dict()
            userdata.append({"data":u.to_dict(),"id":u.id,"user":userdetails})
        pwd = db.collection("tbl_feedback").where("pwd_id", "!=", "").stream()
        for p in pwd:
            pw = p.to_dict()
            pwddetails = db.collection("tbl_pwd").document(pw["pwd_id"]).get().to_dict()
            pwddata.append({"data":p.to_dict(),"id":p.id,"pwd":pwddetails})
        mvd = db.collection("tbl_feedback").where("mvd_id", "!=", "").stream()
        for m in mvd:
            mv = m.to_dict()
            mvddetails = db.collection("tbl_mvd").document(mv["mvd_id"]).get().to_dict()
            mvddata.append({"data":m.to_dict(),"id":m.id,"mvd":mvddetails})
        kseb = db.collection("tbl_feedback").where("kseb_id", "!=", "").stream()
        for k in kseb:
            ks = k.to_dict()
            ksebdetails = db.collection("tbl_kseb").document(ks["kseb_id"]).get().to_dict()
            ksebdata.append({"data":k.to_dict(),"id":k.id,"kseb":ksebdetails})
        municipality = db.collection("tbl_feedback").where("municipality_id", "!=", "").stream()
        for m in municipality:
            mu = m.to_dict()
            municipalitydetails = db.collection("tbl_municipality").document(mu["municipality_id"]).get().to_dict()
            municipalitydata.append({"data":m.to_dict(),"id":m.id,"municipality":municipalitydetails})
        return render(request,"Admin/ViewFeedback.html",{"user":userdata,"pwd":pwddata,"kseb":ksebdata,"municipality":municipalitydata,"mvd":mvddata})
    else:
        return redirect("Guest:login")
    

# Logout
def logout(request):
    del request.session["aid"]
    return redirect("Guest:login")