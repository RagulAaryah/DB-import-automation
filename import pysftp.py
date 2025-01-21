'''
import pysftp
host = 'blvd-kuehdb1901.manhdev.com'
username = 'import_export'
password= 'impexpus3r'
try:
  conn = pysftp.Connection(host=host,port=port,username=username, password=password)
  print("connection established successfully")
except:
  print('failed to establish connection to targeted server')
  '''
import pysftp,getpass,paramiko
if __name__=="__main__":

    try:
        conn = pysftp.Connection(host='',port=22,username="", password="")
        print("connection established successfully")
    except:
        print('failed to establish connection to targeted server') 
'''ṇ
    host= input("enter the hostname or the ip address : ")
    username=input("Gimme the user id : ")      
    port=input("enter the port no : ")
    password = getpass.getpass(prompt = 'Gimme the password : ')ṇ
    try:
        conn = pysftp.Connection(host=host,port=port,username=username, password=password)
        print("connection established successfully")
    except:
        print('failed to establish connection to targeted server') 

'''