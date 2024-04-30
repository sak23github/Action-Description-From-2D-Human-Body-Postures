import mysql.connector as mycon

def connect() : 
    #con=mycon.connect(host='bvj67gg8fecwpx9he6wn-mysql.services.clever-cloud.com',user='ud6sj5ow3oyzcj4b',password='YkjvfizxxHr7S93pLvjN',database='bvj67gg8fecwpx9he6wn')
    con=mycon.connect(host='bjejff4ogwfgzj8m0yww-mysql.services.clever-cloud.com',user='uoqxzraocrsej1sh',password='0bpfquct1WUhLUdm6Q8X',database='bjejff4ogwfgzj8m0yww')
    return con
def getStates():
    conn = connect()
    #integrated security 
    cursor = conn.cursor() 
    cursor.execute('select state from statemaster;')
    data=cursor.fetchall()
    return data