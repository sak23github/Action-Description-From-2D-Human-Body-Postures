import mysql.connector as mycon
import base64
import os

import urllib.request
 
from . import DBOperations
 
import functools 
"""
def connect() : 
    con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    return con
"""
def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='bjejff4ogwfgzj8m0yww-mysql.services.clever-cloud.com',user='uoqxzraocrsej1sh',password='0bpfquct1WUhLUdm6Q8X',database='bjejff4ogwfgzj8m0yww')
    return con
def login1(userid="NA",pass1="NA") : 
    val='NA'
    auth="failed"
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('userlogin1', args)
    print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        auth="success"
        print(result.fetchall())
    conn.commit()
     
    conn.close()
    return auth
def getStates():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select state from statemaster;')
    data=cursor.fetchall()
    conn.close()
    return data

def getDocs2(query="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    print("qr="+"select docid,userid,title,docdesc,dt,tm,filepath,convert((aes_decrypt(skey,docid)),char(900)) from documents where docid in (select docid from keywords1 where keyw like '%"+encrypKeyw(query)+"%')")
    cursor.execute("select docid,userid,title,docdesc,dt,tm,filepath,convert((aes_decrypt(skey,docid)),char(900)) from documents where docid in (select docid from keywords1 where keyw like '%"+encrypKeyw(query)+"%' or title like '%"+(query)+"%')")
    data=cursor.fetchall()
    #print(data[0][0])
    conn.close()
    return data
def getDocs1(userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select docid,userid,title,docdesc,dt,tm,filepath,convert((aes_decrypt(skey,docid)),char(900)) from documents where userid='"+userid+"'")
    data=cursor.fetchall()
    #print(data[0][0])
    conn.close()
    return data
def getUsers():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select usernm,mobileno,emailid,addr,pincode from userdetails;')
    data=cursor.fetchall()
    conn.close()
    return data
def getrent(mon=0,yr=0,userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    print("qr="+"select action,(count(*)*1) as rent from usagelog   where actiondt like '%/"+str(mon)+"/"+str(yr)+"' and userid='"+userid+"' group by action")
    cursor.execute("select action,(count(*)*1) as rent from usagelog   where actiondt like '%/"+str(mon)+"/"+str(yr)+"' and userid='"+userid+"' group by action")
    data=cursor.fetchall()
    conn.close()
    return data
def getCities(state="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select city from cities where state='"+state+"'")
    data=cursor.fetchall()
    conn.close()
    return data
def handle_uploaded_file(f,docid,key,title="nA",desc="NA"):
    nm,ext=os.path.basename(f.name).split('.')
    print("nm="+nm+" "+ext)
    with open('../yoga_pose_detection_webapp/static/Uploads/temp/'+str(docid)+"."+ext, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
    uploaded_file_path='../yoga_pose_detection_webapp/static/Uploads/temp/'+str(docid)+"."+ext
    data=TextExtractionFromPDF.docToText(uploaded_file_path)
            #data="hi how are you"
            #print("path="+uploaded_file_path)
    data1=TextPreProcessing.removeSpaces(data.strip())
            #print(data1.strip())
    filename=str(docid)+"."+ext
    docidtuple=DBOperations.insertFileData(data1.strip(),filename,title,desc,"NA")
    #docid = functools.reduce(lambda sub, ele: sub * 10 + ele, docidtuple) 
            #print(docToText(uploaded_file_path))
    keywords=KeywordsFinder.test(data1.strip(),docid1=docid) 
            #print("document id=")
            #print(docid)
        #print(keywords)
    DBOperations.insertKeywords(keywords)
        #enckeywords(docid)
    DBOperations.updateKeyw("na",docid)
    ECC.encrypt('../yoga_pose_detection_webapp/static/Uploads/temp/'+str(docid)+"."+ext,'../searchable_cloud_enc/static/Uploads/'+str(docid)+"."+ext,key)
    return str(docid)+"."+ext; 
def handle_uploaded_file2(f,userid):
    nm,ext=os.path.basename(f.name).split('.')
    print("nm="+nm+" "+ext)
    with open('../yoga_pose_detection_webapp/static/Photos/'+userid+"."+ext, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
     
    return userid+"."+ext; 
def handle_uploaded_file3(f,userid):
    nm,ext=os.path.basename(f.name).split('.')
    print("nm="+nm+" "+ext)
    id=DBOperations.getMaxId_Postures()
    try:
        os.mkdir("../yoga_pose_detection_webapp/static/Photos/"+userid+"/")
    except Exception:
        print("directory exist")
    with open('../yoga_pose_detection_webapp/static/Photos/'+userid+"/"+str(id)+"."+ext, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
     
    return str(id)+"."+ext; 
def convertFromBase64_Img(base64_message='NA',userid="NA") :
    try:
        os.mkdir("../yoga_pose_detection_webapp/static/Photos/"+userid+"/")
    except Exception:
        print("directory exist")
    id=DBOperations.getMaxId_Postures()
    imgdata = base64.b64decode(base64_message)
    filename = '../yoga_pose_detection_webapp/static/Photos/'+userid+"/"+str(id)+".jpg"  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return str(id)+".jpg"
def getPredictions(userid="NA") : 
    lst=[]
    conn = connect()    
    cursor = conn.cursor()
    #cursor.execute("select* from userprofile where userid='"+uid+"'")
    print("select * from postures where userid='"+userid+"' order by pid desc limit 1")
    sql_select_query = "select * from postures where userid='"+userid+"' order by pid desc limit 1"
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    return record
def getPredictionsHistory(userid="NA") : 
    lst=[]
    conn = connect()    
    cursor = conn.cursor()
    #cursor.execute("select* from userprofile where userid='"+uid+"'")
    print("select * from postures where userid='"+userid+"' order by pid desc")
    sql_select_query = "select * from postures where userid='"+userid+"' order by pid desc"
    cursor.execute(sql_select_query)
    record = cursor.fetchall()    
    return record
def login(userid="NA",pass1="NA") : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('userlogin', args)
    print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        print(result.fetchall())
    conn.commit()
 
    conn.close()
    return val
def insertKeywords(keywDic) : 
     
    conn = connect()    
    mycursor = conn.cursor()
    sql = "INSERT INTO keywords(keyw,score,docid) VALUES (%s, %s,%s)"
    
    mycursor.executemany ( sql, keywDic )

    conn.commit ( )

    #print ( mycursor.rowcount, "was inserted." )
    
    conn.close()
def encrypKeyw(x,k=0):
  return x[::-1]

def convertToBase64(message='NA') :
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
    return base64_message

def convertFromBase64(base64_message='NA') :
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    print(message)
    return message

def insertUser(userid='NA',pass1='NA',name='NA',addr='NA',pincode='NA',mobile="NA",email="NA",gender="Na",dob="NA",state="NA",city="NA",photo="NA") : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1,name,mobile,email,city,state,gender,addr,dob,pincode,photo]
    args1=cursor.callproc('insertUser', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
       # val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
    #print(val[0])
def updatePass(userid='NA',pass1='NA') : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,pass1]
    args1=cursor.callproc('updatePass', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
       # val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
def insertUsageLog(userid='NA',service='NA',dt='NA') : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,service,dt]
    args1=cursor.callproc('insertusage', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
       # val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
    #print(val[0])
def insertDoc1(userid="NA",title="NA",docPath="NA",docDesc='NA',dt="NA",tm="NA",key='NA') : 
    conn = connect()    
    cursor = conn.cursor()
    args = [userid,title,dt,tm,docDesc,key,docPath]
    args1=cursor.callproc('insertDoc', args)
    print("Return value:", args1)
    #for result in cursor.stored_results():
     #       print(result.fetchall())
    cnt=cursor.rowcount 
    conn.commit()
    conn.close()

def deletedoc(docid=0) : 
    conn = connect()    
    cursor = conn.cursor()
    args = [docid]
    args1=cursor.callproc('deleteDoc', args)
    print("Return value:", args1)
    #for result in cursor.stored_results():
     #       print(result.fetchall())
    cnt=cursor.rowcount 
    conn.commit()
    conn.close()


    #args = [userid,title,docPath,docDesc,dt,tm,key]
    #args1=cursor.callproc('insertDoc', args)
    #print("Return value:", args1)
    #for result in cursor.stored_results():
    #        print(result.fetchall())
    #cnt=cursor.rowcount
    
    #return cnt
def getEmail(userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute("select emailid from userdetails where userid='"+userid+"';")
    email="NA"
    for row in cursor: 
        email=row[0]
        print(email)
    conn.close()
    return email 
def getMaxIdDoc1():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select (ifnull(max(docid),1000)+1) as mxid from documents;')
    mxid=0
    for row in cursor: 
        mxid=row[0]
        print(int(mxid)+1)
    conn.close()
    return mxid
def getTotalRent(mon=0,yr=0,userid="NA"):
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    print("qr="+"select action,(count(*)*1) as rent from usagelog   where actiondt like '%/"+str(mon)+"/"+str(yr)+"' and userid='"+userid+"' group by action")
    cursor.execute("select  sum(count(*)*1) as rent from usagelog   where actiondt like '%/"+str(mon)+"/"+str(yr)+"' and userid='"+userid+"' group by action")
   
    #cursor.execute('select (ifnull(max(docid),1000)+1) as mxid from documents;')
    mxid=0
    for row in cursor: 
        mxid=row[0]
        print(int(mxid)+1)
    conn.close()
    return mxid