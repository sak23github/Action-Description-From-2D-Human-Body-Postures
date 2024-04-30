from django.http import HttpResponse
from  django.shortcuts import render
from . import models
import random
import mysql.connector as mycon
from datetime import date
from datetime import datetime
from . import sendMail
from . import img_Detection
import ast
from django import template
register = template.Library()
def index(request):
    data= models.getStates()
    return render(request, "index.html",{"list":data})
def sendotp1(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")  
        email=request.POST.get("email")  
        val=models.login1(userid,email) 
        if val=='success':
            otp=str(random.randint(1111,9999))
            print("otp="+otp)
            request.session['otp']=otp
            sendMail.sendotp(otp,email)
            return render(request, "otpverification2.html",{"userid":userid,"email":email})
        else:
            return render(request, "Success.html",{"mess":"Authentication Failed!!"})
def forgot(request): 
    return render(request, "passwordRecovery.html")
def takephoto(request): 
    return render(request, "takePhoto.html")
def submitPhoto(request):
    if request.method == 'POST':
        image=request.POST.get("photo") 
        userid= request.session['userid']  
        str2,str1=image.split(',')
        photo=models.convertFromBase64_Img(str1,userid)
        id,ext=photo.split('.')
        id1=int(id.strip())
        img_Detection.pose_prediction(userid+"/"+photo,userid+"/1_"+photo,id1,userid)
        print("id="+str(id1))         
        #models.insertPosture(userid,pswd,usernm,addr,pincode,mobileno,emailid,gender,dob,state,cities,photo)
    data= models.getPredictions(userid)
    print(data)
    lst=[]
    if str(data[0][5]) == 'NA':
        lst=[]
    else :
        lst = ast.literal_eval(str(data[0][5]))
    print("lst")
    print(lst)
    return render(request, "Predictions.html",{"list":data,"suglst":lst})  
        
def upload(request): 
    return render(request, "UploadPose.html")
def user(request):
    userid= request.session['userid']  
    data= models.getPredictionsHistory(userid)
    return render(request, "user.html",{"list":data})
def admin(request): 
    data= models.getUsers()
    return render(request, "admin.html",{"list":data}) 
def logout(request):
    del request.session["user"]  
    data= models.getStates()
    return render(request, "index.html",{"list":data})
    
 
def otpverification1(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")  
        email=request.POST.get("email")  
        seckey=request.POST.get("seckey")  
        otp=request.POST.get("otp")  
        otp1=request.session['otp']
        pass1=str(random.randint(1111,9999))
        if otp==otp1:
            models.updatePass(userid,pass1)
            sendMail.sendotp1(pass1,email)
            return render(request, "Success.html",{"mess":"Password Sent on Email Successully..."}) 
        else:
            return render(request, "Success.html",{"mess":"OTP Authentication Failed!!"})
             
                
        
def sendotp(request):
    if request.method == 'POST':
        docid=request.POST.get("docid")  
        docpath=request.POST.get("docpath")  
        seckey=request.POST.get("seckey")  
        emailid= request.session['emailid']
        otp=str(random.randint(1111,9999))
        request.session['otp']=otp
        sendMail.sendotp(otp,emailid)
        today = date.today()
        dt= today.strftime("%d/%m/%Y")
        models.insertUsageLog(request.session["userid"],'email',dt)
        return render(request, "otpauth.html",{"docid":docid,"docpath":docpath,"seckey":seckey})
 
    
def Cities(request):
    data= models.getCities(request.GET.get("state"))    
    return render(request, "cities.html",{"list":data})
 
def login(request):
    if request.method == 'POST':
        userid=request.POST.get("userid") 
        pass1=request.POST.get("pass") 
        val=models.login(userid,pass1)
        if(len(val)>0): 
            request.session["user"]={"userid":val[0][0],"utype":val[0][3],"username":val[0][2]}    
            request.session["userid"]=val[0][0] 
            request.session["emailid"]=models.getEmail(val[0][0])   
            if val[0][3]=="admin":
                data= models.getUsers()
                return render(request, "admin.html",{"list":data})             
            elif val[0][3]=="user":
                data= models.getPredictionsHistory(userid)
                return render(request, "user.html",{"list":data})
            else:
                return render(request, "Success.html",{"mess":"Authentication Failed!!"}) 
        else:
            return render(request, "Success.html",{"mess":"Authentication Failed!!"}) 
def registeruser(request):
    if request.method == 'POST':
        userid=request.POST.get("userid")   
        usernm=request.POST.get("usernm")
        pswd=request.POST.get("pswd")
        emailid=request.POST.get("emailid")
        mobileno=request.POST.get("mobileno")
        gender=request.POST.get("gender")
        pincode=request.POST.get("pincode")
        addr=request.POST.get("addr")
        state=request.POST.get("state")
        cities=request.POST.get("cities")
        dob=request.POST.get("dob")
        print(userid)
        print(usernm)
        print(pswd)
        print(emailid)
        photo=models.handle_uploaded_file2(request.FILES['file'],userid)
                 
        models.insertUser(userid,pswd,usernm,addr,pincode,mobileno,emailid,gender,dob,state,cities,photo)
    return render(request, "Success.html",{"mess":"Your Registration Done Successfully..."})
def uploadPose(request):
    if request.method == 'POST':
        userid= request.session['userid'] 
         
        print(userid)
        
        photo=models.handle_uploaded_file3(request.FILES['file'],userid)
        id,ext=photo.split('.')
        id1=int(id.strip())
        img_Detection.pose_prediction(userid+"/"+photo,userid+"/1_"+photo,id1,userid)
        print("id="+str(id1))         
        #models.insertPosture(userid,pswd,usernm,addr,pincode,mobileno,emailid,gender,dob,state,cities,photo)
    data= models.getPredictions(userid)
    print(data)
    lst=[]
    if str(data[0][5]) == 'NA':
        lst=[]
    else :
        lst = ast.literal_eval(str(data[0][5]))
    print("lst")
    print(lst)
    return render(request, "Predictions.html",{"list":data,"suglst":lst}) 
    #return render(request, "Prediction.html",{"mess":"Your Registration Done Successfully..."})
@register.filter(name="get_string_as_list") # register the template filter with django
def get_string_as_list(value): # Only one argument.
    """Evaluate a string if it contains []"""
    lst=[]
    print("from filter")
    print(value)
    if '[' and ']' in value:
        return eval(value)
    else:
        return lst
register.filter('get_string_as_list', get_string_as_list)