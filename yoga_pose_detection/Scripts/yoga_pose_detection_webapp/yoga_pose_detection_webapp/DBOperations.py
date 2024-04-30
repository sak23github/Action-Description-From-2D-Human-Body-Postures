 
from . import DBConnect 
import base64
import mysql.connector as mycon
 
def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='bjejff4ogwfgzj8m0yww-mysql.services.clever-cloud.com',user='uoqxzraocrsej1sh',password='0bpfquct1WUhLUdm6Q8X',database='bjejff4ogwfgzj8m0yww')
    return con
 
    
 
def insertPosture(id=0,userid='NA',predicted_pose='NA',suggestion='NA',imgpath='NA') : 
    val='NA'
    conn = connect()    
    cursor = conn.cursor()
    print("iiiid= ")
    print(id)
    print(suggestion)
    args = [int(id),userid,suggestion,imgpath,predicted_pose]
    args1=cursor.callproc('insertPosture', args)
    #print("Return value:", args1)
    for result in cursor.stored_results():
        val=result.fetchall()
        #print(result.fetchall())
    conn.commit()
    conn.close()
    #print(val[0])
    return(val[0]) 

    
 
def getMaxId_Postures():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select (ifnull(max(pid),1000)+1) as mxid from postures;')
    mxid=0
    for row in cursor: 
        mxid=row[0]
        print(int(mxid)+1)
    conn.close()
    return mxid    

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

 