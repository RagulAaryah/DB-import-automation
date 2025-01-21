#from asyncio.log import logger
import cx_Oracle,sys,logging,paramiko,os,pysftp,subprocess,socket
from paramiko import SFTP, SSHClient



class DB:
    
    def __init__(self):

        print("======================================Kill DB session script==========================")
        #uid,pwd,host,port,service_name
        #print("Connection protocol : currentClassObject.MakeConnection(uid='Fill username',pwd='Fill password',host='Fill hostname',portno='Fill port number,service_name='Fill service name''")
        #print("\n")

    def close_con(self,connection):
        if str(type(connection)) in ("<class '__main__.DB'>","<class 'cx_Oracle.Cursor'>","<class 'cx_Oracle.Connection'>"):
            connection.cursor.close()
            connection.DB_con.close()
        else:
            connection.close()
    
    def noConnection(self,connection):
        return True if connection is None else False

    def getCredentials(self):
        con_str=input("enter  connection string of format : 'username password host portno service_name : '")
        con_str_split=con_str.strip().split(" ")
        return con_str_split

    def setArgsList(self,Args):
        #print("=========================inside set args list function================================\n")
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Arguments List:', str(sys.argv))
        self.logger.info(str('Arguments List : '+str(sys.argv)))
        #print("args set ")
        print("\n")
        return Args[1:]
        
    def DefineLogger(self,f_name):
        #print("=========================inside Define Logger method===================================\n")
        logging.basicConfig(filename=f_name,
					format='%(asctime)s %(message)s',
					filemode='w')
    
        # Creating an object
        self.logger = logging.getLogger()
        #logging.getLogger("paramiko").setLevel(logging.DEBUG) 

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

        print("logger configured\n")

    def MakeConnection(self,uid,pwd,host,port,service_name):

        #print("==========================Trying to make a connection================================\n")
        #conn_str=dbuser+"/"+dbpassword+"@"+dbhostname+":"+dbport+"/"+dbservicename
        self.uid=uid
        conn_str=uid+"/"+pwd+"@"+host+":"+port+"/"+service_name
        print("connection string : "+conn_str)
        self.DB_con=cx_Oracle.connect(conn_str)
        self.cursor=self.DB_con.cursor()
        if self.cursor is not None:
            print("DB connection is successful !")
            self.logger.info("DB connection is successful !")
            print("DB version : "+self.DB_con.version)
            self.logger.info("DB version : "+self.DB_con.version)
            print("\n")
        else:
            print("connection failed\n")
            self.logger.error("connection failed")
            #print("DB connection successful !!")
    
    def disp_proc(self,procedure):
        #print("================================executing the procedure====================================\n")
        if self.cursor is not None:
            try:
                #print("===============================enabling the dbms output==============================")
                # enable DBMS_OUTPUT
                self.cursor.callproc("dbms_output.enable")
                print("\n")
                #print("enabled dbms_ouput.putline command !")
                #self.logger.info("enabled dbms_ouput.putline command !")
            except cx_Oracle.Error as e:
                self.logger.info(e)
                print("unable to enable dbms output line : "+str(e))
            #self.cursor.callproc("manh_show_sessions")
            try:
                #print("===========================formatting for using dbms_output============================")
                # execute some PL/SQL that calls DBMS_OUTPUT.PUT_LINE
                self.cursor.callproc(procedure)
                # tune this size for your application
                chunk_size = 100
                # create variables to hold the output
                self.lines_var = self.cursor.arrayvar(str, chunk_size)
                self.num_lines_var = self.cursor.var(int)
                self.num_lines_var.setvalue(0, chunk_size)
            except Exception as e:
                self.logger.error(str(e))
                print("Exception : "+str(e))

            try:
                #print("=============printing output using dbms output=======================")
                # fetch the text that was added by PL/SQL
                #with open("dataPump.txt", "w+") as self.file1:
                    #self.logger.info("created a new file for the table")
                while True:
                    self.cursor.callproc("dbms_output.get_lines", (self.lines_var, self.num_lines_var))
                    self.num_lines = self.num_lines_var.getvalue()
                    self.lines = self.lines_var.getvalue()[:self.num_lines]
                    self.logger.info("\n\n"+"="*24+"Active sessions"+"="*24)
                    for line in self.lines:
                        print(line or "")
                        
                        self.logger.info(str(line))
                        '''
                        try:
                            self.file1.writelines(line+"\n")

                        except Exception as e:
                            print("Exception : "+str(e))
                            self.logger.error(str(e))
                        '''
                    if self.num_lines < chunk_size:
                        break   
                    self.logger.info("\n"+"="*63)
            except Exception as e:
                print("Exception : "+str(e))
                self.logger.error(str(e))
           
        else:
            print("there's no connection to the database !\n")
            self.logger.error("no connection to the database")
    
    def exec_proc(self,procedure):
        #self.disp_proc(procedure)
        if self.cursor is not None:
            self.disp_proc("manh_show_sessions")
            #machine=str(os.environ.get('USERNAME')
            command=''' 
                        select SID,SERIAL#,USERNAME,SCHEMANAME,OSUSER,MACHINE
                        from v$session
                        where schemaname = '''+str(self.uid)+'''
                        and type = 'USER'
                        and username not in ('SYS','SYSTEM')
                    '''
            
            try:
                self.cursor.execute(command)
                sess=list(self.cursor.fetchall())
                for i in sess:
                    print()
                #print("Active sessions fetched successfully")
                #self.logger.info("Active sessions fetched successfully")                
                try:
                    for i in range(0,len(sess),1):
                        #print(f"trying to kill session {sess[i][0]}")
                        try:
                            self.cursor.callproc("manh_kill_session",[sess[i][0],sess[i][1]])
                            print(f"successfully shutdown session : {sess[i][0]} ")
                            self.logger.info("successfully shutdown session : "+str(sess[i][0]))
                        except Exception as e:
                            if str(e)[:38]=="ORA-00027: cannot kill current session":
                                pass
                            else:
                                print(f"while kill the session {sess[i][0]} encountered an issue : "+str(e))
                                self.logger.error(f"while killing the session {sess[i][0]} encountered an issue : "+str(e))
                except Exception as e:
                    print("Exception while execution of kill session : "+str(e))
                    self.logger.error(str(e))

            except Exception as e:
                print("Error : "+str(e))
                self.logger.error(str(e))
            
            
        else:
            print(f"Error while executing procedure :{procedure} , Database not connected ")
            self.logger.error(f"Error while executing procedure :{procedure} , Database not connected ")

    

class WM_apps_stop(DB):

    def __init__(self):
        print("=======================================WM_MDA_MIP stop script==========================================================")
        #print("Connection protocol : currentClassObject.MakeConnection(host='Fill hostname')")
        self.connection=False
       
    def DefineLogger(self,f_name):
        #print("=========================inside Define Logger method===================================\n")
        logging.basicConfig(filename=f_name,
					format='%(asctime)s %(message)s',
					filemode='w')
    
        # Creating an object
        self.logger = logging.getLogger()
        #logging.getLogger("paramiko").setLevel(logging.DEBUG) 

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

        print("logger configured\n")
    def noConnection(self, connection):
        return super().noConnection(connection)
    
    def getCredentials(self):
        host=input("enter the hostname : ")
        return host 

    def MakeConnection(self,host):
        #creating an instance of client
        self.client = SSHClient()
        #establishing a connection 
        if self.connection==False:
            try:
                #client.connect(str(hostname=arglist[0]).strip(),username="wmsadmin",port=22, password="wmsadmin")
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(hostname=host,username='wmsadmin',password='wmsadmin')
                print("Successfully logged into the Host : "+host+"  !")
                self.logger.info("Successfully logged into the Host : "+host+"  !")
                self.connection=True
            except paramiko.AuthenticationException:
                print("Authentication failed, please verify your credentials for the WM host `")
                self.logger.info("Authentication failed, please verify your credentials for WM host")
            except paramiko.SSHException as sshException:
                print("Could not establish SSH connection: %s" % sshException)
                self.logger.info("Could not establish SSH connection: %s" % sshException)
                
            except socket.timeout as e:
                print("Connection timed out")
                self.logger.info("Connection timed out")
                
            except Exception as e :    
                self.logger.error("connection to the "+host+" failed due to the error : "+str(e))
                sys.exit(-1)
        else:
            print("connection already exists !")
            self.logger.info("connection already exists !")
    
    def stop_WM_app(self):

        print("checking if connected to the host ...")
        self.logger.info("checking if connected to the host ...")

        if self.connection==True:
            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            try:
                command_string= "cd /apps/scope/products/WM/tools/bin; sh manageserver.sh stop wms"
                '''
                #print(command_string)
                #channel = client.get_transport().open_session()
                #channel.exec_command('cd /apps/scope/products/WM/tools/bin')
                #stdin, stdout, stderr = channel.exec_command('cd /apps/scope/products/WM/tools/bin')
                #b=str(stdout.read())
                #stop="./"+arglist[1]+" stop wms"
                #(stdin,stdout, stderr) = client.exec_command(command_string)
                '''
                print("\n===============================attempting to stop WM application=====================================================\n")
                self.logger.info("invoking the action : "+command_string)
                (stdin,stdout,stderr) = self.client.exec_command('')
                a=str(stderr.read())
                #print(a)
                #print("executed the command !")
                if a=="b''":
                    self.logger.info("status : Successfully shutdown WM application !")
                    print("status : Successfully shutdown WM application !")
                else:
                    self.logger.info("Error during execution , cause : "+a) 
                print("=======================================================================================================================")
            except Exception as e:
                self.logger.error("error in execution of the cd , cause :"+str(e))
                self.close_con(self.client)
                self.connection=False
                sys.exit(-1)
        else:
            print("connection doesn't exist make sure to have the connection established to stop the WM application !")
            self.logger.info("connection doesn't exist make sure to have the connection established to stop the WM application !")

    def stop_MDA_app(self):
        print("checking if connected to the host ...")
        self.logger.info("checking if connected to the host ...")
        if self.connection==True:
            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            try:
                print("\n================================attempting to stop MDA application===================================================\n")
                command_string= 'cd /apps/scope/products/MDA/distribution/DeploymentDirector/installer;'+"sh "+"./scpp-ant.sh stop"
                self.logger.info("invoking the action : "+command_string)
                (stdin,stdout, stderr) = self.client.exec_command(command_string)
                a=str(stderr.read())
                #print("executed the command !")

                if a=="b''":
                    self.logger.info("status : Successfully shutdown MDA application !")
                    print("status : Successfully shutdown MDA application !")
                else:
                    print("Error during execution , cause : "+a)
                    self.logger.info("Error during execution , cause : "+a) 
                print("======================================================================================================================")
            except Exception as e:
                self.logger.error("error in execution of the cd ,cause : "+str(e))
                self.close_con(self.client)
                self.connection=False
                sys.exit(-1)
        else:
            print("connection doesn't exist make sure to have the connection established to stop the MDA application !")
            self.logger.info("connection doesn't exist make sure to have the connection established to stop the MDA application !")            

    def stop_MIP_app(self):

        print("checking if connected to the host ...")
        self.logger.info("checking if connected to the host ...")

        if self.connection==True:
    
            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            try:
                print("===================================attempting to stop MIP application================================================\n")
                command_string= 'cd /apps/scope/products/MIP/distribution;'+"./scpp-ant.sh stop"
                '''
                #print(command_string)
                #channel = client.get_transport().open_session()
                #channel.exec_command('cd /apps/scope/products/WM/tools/bin')
                #stdin, stdout, stderr = channel.exec_command('cd /apps/scope/products/WM/tools/bin')
                #b=str(stdout.read())
                #stop="./"+arglist[1]+" stop wms"
                #(stdin,stdout, stderr) = client.exec_command(command_string)
                '''
                self.logger.info("invoking the action : "+command_string)
                (stdin,stdout, stderr) = self.client.exec_command(command_string)
                a=str(stderr.read())
                
                if a=="b'     [exec] Result: 1\\n'":
                    self.logger.info("status : Successfully shutdown MIP application !")
                    print("status : Successfully shutdown MIP application !")
                else:  
                    print("Error during execution , cause : "+a)
                    self.logger.info("Error during execution , cause : "+a) 
                print("====================================================================================================================")

            except Exception as e:
                self.logger.error("error in execution of the cd , cause : "+str(e))
                self.close_con(self.client)
                self.connection=False
                sys.exit(-1)

        else:
            print("connection doesn't exist make sure to have the connection established to stop the MIP application !")
            self.logger.info("connection doesn't exist make sure to have the connection established to stop the MIP application !")
    
    def close_con(self,connection):
        return super().close_con(connection)

    def killOrphansPIDs_old(self):
        print("checking if connected to the host ...")
        self.logger.info("checking if connected to the host ...")
        if self.connection==True:

            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            try:
                print("===============================attempting to fetch orphan PIDs=======================================")
                (stdin,stdout, stderr) = self.client.exec_command("ps -ef")
                #process_match="b'wmsadmin  "
                process_match="b'wmsadmin  '"
                PIDs=stdout.read().splitlines()
                


                for i in PIDs:
                    print(i)
                #print("length :\n\n\n"+str(len(PIDs)))
                for i in range(1,len(PIDs),1):
                    try:
                        #pid=int(PIDs[i][9:15])
                        #print("sliced string  wmsadmin :  "+str(PIDs[i][:10]))
                        #print("sliced string WMS process id : "+str(pid) )
                        
                        uid_slice=str(PIDs[i][:10])
                        print("if "+uid_slice+"=="+process_match)
                        if uid_slice==process_match:
                            print("killing the orphan!")
                            pid=int(PIDs[i][9:15])

                            (stdin,stdout, stderr) = self.client.exec_command("kill -9 "+str(pid))
                            print(str(stderr.read()))
                            if str(stderr.read())=="b''":
                                print("no error")
                            #print("output after killing orphan "+str(stderr.read())+" ")                            
                            #print("errors or exceptions while killing the orphan "+str(stderr.read()))
                            #self.logger.info("errors or exceptions while killing the orphan "+str(stderr.read()))
                            #self.logger.info("output after killing orphan "+str(stdout.read())+" ")
                        else:
                            print("uid doesn't match!")
                    except Exception as e:
                        print("error while killing sessions "+str(e))
                        sys.exit(-1)
                #print("errors found "+a)
            except Exception as e:
                print("error : "+str(e))
                self.logger.error("error : "+str(e))
        else:
            self.logger.info("connection doesn't exist , make sure to establish a connection ")
            print("connection doesn't exist , make sure to establish a connection ")


    def killOrphansPIDs(self):
        print("checking if connected to the host ...")
        self.logger.info("checking if connected to the host ...")
        if self.connection==True:

            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            try:
                print("\n===============================attempting to fetch orphan PIDs=======================================")
                (stdin,stdout, stderr) = self.client.exec_command(" ps -eaf | grep -i /apps/scope/products")
                #process_match="b'wmsadmin  "
                
                PIDs=stdout.read().splitlines()      


                for i in PIDs:
                    print(i)
                if len(PIDs)>=1:
                    for i in range(0,len(PIDs),1):
                        try:  

                            #print("killing the orphan!")
                            pid=int(PIDs[i][9:15])

                            (stdin,stdout, stderr) = self.client.exec_command("kill -9 "+str(pid))
                            #print(str(stderr.read()))
                            if str(stderr.read()=="b'bash: line 0: kill: (47855) - No such process\\n'"):
                                pass
                                #print("this was the current process to check and kill the orphan processes")
                                #self.logger.info("this was the current process to check and kill the orphan processes")
                            
                            elif str(stdout.read())=="b''":
                                print("no issues in killing the orphan "+str(pid)) 
                                self.logger.info("no issues in killing the orphan "+str(pid))
                            
                            else:
                                print(f"Encountered the error while killing the orphan {str(pid)} : {str(stderr.read())}")                              
                                self.logger.error("Encountered the error while killing the orphan "+str(pid)+" : "+str(stderr.read()))
                        except Exception as e:
                            print("error while killing sessions "+str(e))
                            self.logger.info("error while killing sessions "+str(e))
                            sys.exit(-1)
                    #print("errors found "+a)
                else:
                    print("Active sessions : 0")
                    self.logger.info("Active sessions : 0")
            except Exception as e:
                print("error : "+str(e))
                self.logger.error("error : "+str(e))
        else:
            self.logger.info("connection doesn't exist , make sure to establish a connection ")
            print("connection doesn't exist , make sure to establish a connection ")
class DB_dump_download(DB):

    def __init__(self):
        print("\n==============================================DB dump download script===============================================")
        #print("Connection protocol : currentClassObject.MakeConnection(uid='Fill username',pwd='Fill password',portno='Fill port number'")
        self.connection=False

    def DefineLogger(self,f_name):
        #print("=========================inside Define Logger method===================================\n")
        logging.basicConfig(filename=f_name,
					format='%(asctime)s %(message)s',
					filemode='w')
    
        # Creating an object
        self.logger = logging.getLogger()
        #logging.getLogger("paramiko").setLevel(logging.DEBUG) 

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.INFO)

        print("logger configured\n")

    def close_con(self, connection):
        return super().close_con(connection)
    
    def getCredentials(self):
        con_str=input("enter the connection string of format : 'username password portno : '")
        con_str_split=con_str.strip().split(" ")
        return con_str_split

    def MakeConnection(self, uid, pwd,Db_host):
        
        if self.connection==False:
            self.uid=uid
            self.pwd=pwd
            self.host=Db_host
            self.MAthruHost="ord1-ftp.thruinc.net"
            try:
                print("=================================Attempting to connect to DB_host==========================================\n")
                self.ssh_db = SSHClient()
                self.ssh_db.load_system_host_keys()
                self.ssh_db.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_db.connect(hostname=Db_host, username="import_export", password="impexpus3r")
                #self.ssh.connect('maftp.thruinc.net', username=uid, password=pwd)
                # or 
                # key = paramiko.RSAKey.from_private_key_file('id_rsa')
                # ssh.connect(host, username='user', pkey=key)
                self.logger.info("connected to the DB host : "+self.host+" successfully")
                print("connected to the DB host : "+self.host+" successfully")
                
                self.ssh_Ma=SSHClient()
                self.ssh_Ma.load_system_host_keys()
                self.ssh_Ma.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_Ma.connect(hostname=self.MAthruHost,username="maftp.thruinc.net\\"+self.uid,password=self.pwd)
                print("successfully connected to the host : "+self.MAthruHost)
                try:    
                    self.ma_sftp=self.ssh_db.open_sftp()
                    print("MAthru sftp connection opened ")
                except Exception as e:
                    print("unable to open sftp in DB due to the error : "+str(e))
                    self.logger.error("unable to open sftp in DB due to the error : "+str(e))
                try:
                    self.db_sftp=self.ssh_Ma.open_sftp()
                    print("sftp connection is opened up for the DB host ")
                except Exception as e :
                    print("unable to open sftp in MAthru due to the error : "+str(e))
                    self.logger.info("unable to open sftp in MAthru due to the error : "+str(e))
                self.connection=True
                print("set connection to be true ")
            
            except paramiko.AuthenticationException:
                print("Authentication failed, please verify your credentials for DB host "+self.host)
                self.logger.info("Authentication failed, please verify your credentials for DB host "+self.host)
                
            except paramiko.SSHException as sshException:
                print("Could not establish SSH connection: %s" % sshException)
                self.logger.info("Could not establish SSH connection: %s" % sshException)
                
            except socket.timeout as e:
                print("Connection timed out")
                self.logger.info("Connection timed out")
                

            except Exception as e:
                print("connection failed ! , cause :"+str(e))
                self.logger.error("connection failed ! , cause :"+str(e))
        else:
            print("sftp connection already exists ! ")
            self.logger.info("sftp connection already exists ! ")
    def getPathDetails(self):
            return input("enter the details in the format : client_folder remaining_path filename download_path :").strip().split()
        

    #def download_dump(self,client_folder,remaining_path,filename,download_path):
    def download_dump(self):
        
        #details=self.getDetails()
        print("checking if sftp connection exists...")
        self.logger.info("checking if sftp connection exists...")
        
        if self.connection==True:
            print("Good to go ! connection exists ")
            self.logger.info("Good to go ! connection exists ")
            file_loc="/COMMON/FromManh/"+str(sys.argv[3]+"/"+sys.argv[4]+"/"+sys.argv[5])
            print("file name with location : "+file_loc)
            try:
                with self.ma_sftp.open("/COMMON/FromManh/"+str(sys.argv[3]+"/"+sys.argv[4]+"/"+sys.argv[5])) as f:
                    # putfo takes an open file object and creates it at the specifies path
                    self.db_sftp.putfo(f,"/data/dump/")  # need filename

                    self.ma_sftp.close()
                    self.db_sftp.close()
            except Exception as e:
                print("error while downloading the file , error : "+str(e))
            
                self.connection=False
                sys.exit(-1)
        else:
            print("sftp conneciton doesn't' exist make sure connection is established ")
            self.logger.info("sftp conneciton doesn't' exist make sure connection is established ")

    
    
if __name__=="__main__":
    
    print("\n\nEnsuring mandatory packages are installed ")
    package_list=['cx_Oracle','paramiko','pysftp']
    for package in package_list:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package],stdout=subprocess.DEVNULL)
    print("\n========================================================================================")
    
    print('\nNumber of arguments : '+str(len(sys.argv))+' arguments.')
    print('Arguments List : '+ str(sys.argv))


    dload_dump=DB_dump_download()
    #f_path_name="C:/Users/rpalanisamy/Documents/PyScript/logs/SFTP_logs.log"
    dload_dump.DefineLogger("DB_Import_Log.txt")
    dload_dump.logger.info("\n=============================SFTP connection========================================")
    dload_dump.logger.info('Number of arguments : '+str(len(sys.argv))+' `arguments.')
    dload_dump.logger.info('Arguments List : '+ str(sys.argv[:2]+sys.argv[3:]))
    #con_str_split=dload_dump.getCredentials()
    dload_dump.MakeConnection(Db_host=sys.argv[9],uid=sys.argv[1],pwd=sys.argv[2])
    dload_dump.download_dump()



    stop_app=WM_apps_stop()
    #f_path_name="C:/Users/rpalanisamy/Documents/PyScript/logs/Stop_WM_MDA_MIP_LOG.log"
    #f_path_name=input("enter the name of the log with the directory or without : ")
    stop_app.DefineLogger("stop_WM_MDA_MIP_LOG")
    stop_app.logger.info("\n=============================Stopping the applicaitions==============================")
    stop_app.MakeConnection(host=sys.argv[6])
    stop_app.stop_WM_app()
    stop_app.stop_MDA_app()
    stop_app.stop_MIP_app()
    stop_app.killOrphansPIDs()
    stop_app.client.close()
    #stop_app.logger.close()
    
    kill_sess=DB()
    #kill_sess.print_arg_list()
    f_path_name="C:/Users/rpalanisamy/Documents/PyScript/logs/kill_DB_sessions_LOG.log"
    #f_path_name=input("enter the name of the log with the directory or without : ")
    kill_sess.DefineLogger("kill_DB_sessionsLog")
    kill_sess.logger.info("\n===========================Killing DB sessions ======================================")

    #arglist=kill_sess.setArgsList(sys.argv)
    #self,uid,pwd,host,port,service_name
    #con_str_split=kill_sess.getCredentials()
    kill_sess.MakeConnection(uid=sys.argv[7],pwd=sys.argv[8],host=sys.argv[9],port=sys.argv[10],service_name=sys.argv[11])
    #kill_sess.logger.info(str(os.environ['COMPUTERNAME']))
    #print(str(os.environ['COMPUTERNAME']))
    kill_sess.exec_proc("manh_show_sessions")
    kill_sess.close_con(kill_sess)

#https://stackoverflow.com/questions/69950605/how-to-transfer-zip-files-from-one-server-to-another-using-python-sftp-paramiko