from asyncio.log import logger
import cx_Oracle,sys,logging
# importing panda library


class DB:
    '''
    def __init__(self,host,uid,pwd,port,service_name):
        self.hostname=host
        self.username=uid
        self.password=pwd
        self.port=port
        self.service_name=service_name
    '''
    def setArgsList(self,Args):
        #print("=========================inside set args list function================================\n")
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Arguments List:', str(sys.argv))
        logger.info(str('Arguments List : '+str(sys.argv)))
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
        self.logger.setLevel(logging.DEBUG)

        print("logger configured\n")
    def MakeConnection(self,uid,pwd,host,port,service_name):
        self.uid=uid
        #print("==========================Trying to make a connection================================\n")
        #conn_str=dbuser+"/"+dbpassword+"@"+dbhostname+":"+dbport+"/"+dbservicename
        conn_str=uid+"/"+pwd+"@"+host+":"+port+"/"+service_name
        print("connection string : "+conn_str)
        self.DB_con=cx_Oracle.connect(conn_str)
        self.cursor=self.DB_con.cursor()
        if self.cursor is not None:
            print("DB connection is successful !")
            logger.info("DB connection is successful !")
            print("DB version : "+self.DB_con.version)
            logger.info("DB version : "+self.DB_con.version)
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
                print("enabled dbms_ouput.putline command !")
                self.logger.info("enabled dbms_ouput.putline command !")
            except cx_Oracle.Error as e:
                logger.info(e)
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
                print("=============printing output using dbms output=======================")
                # fetch the text that was added by PL/SQL
                with open("dataPump.txt", "w+") as self.file1:
                    self.logger.info("created a new file for the table")
                    while True:
                        self.cursor.callproc("dbms_output.get_lines", (self.lines_var, self.num_lines_var))
                        self.num_lines = self.num_lines_var.getvalue()
                        self.lines = self.lines_var.getvalue()[:self.num_lines]
                        for line in self.lines:
                            print(line or "")
                            try:
                                self.file1.writelines(line+"\n")

                            except Exception as e:
                                print("Exception : "+str(e))
                                self.logger.error(str(e))
                        if self.num_lines < chunk_size:
                            break
        
                    
            except Exception as e:
                print("Exception : "+str(e))
                self.logger.error(str(e))
           
        else:
            print("there's no connection to the database !\n")
            self.logger.error("no connection to the database")
    
    def exec_proc(self,procedure):
        self.disp_proc(procedure)
        if self.cursor is not None:
            try:
                self.result=self.cursor.execute(''' 
    begin
    select  sid , serial#  from v$session
    where schemaname = USER
    and type = 'USER'
    and username not in ('SYS','SYSTEM');
    ALTER SYSTEM KILL SESSION 'sid,'
    end;
            ''')
                print("Active sessions fetched successfully")
                self.logger.info("Active sessions fetched successfully")
            except Exception as e:
                print("Error : "+str(e))
                self.logger.error(str(e))
        
            #print("==============================Attempting to kill the sessions===================================")
            #print("Active Processes : "+str(self.result.fetchall()))
            #print("type of the above ouput : "+str(type(self.result)))
            #print("trying to convert result into list "+str(list(self.result)))
            
            self.disp_proc(procedure)
        else:
            print(f"Error while executing procedure :{procedure} , Database not connected ")
            self.logger.error(f"Error while executing procedure :{procedure} , Database not connected ")

if __name__=="__main__":
    
    print("=============== 1.STOP WM / MDA / MIP application ========================")
    print("=============== 2.Kill DB Sessions =======================================")
    choice =int(input("enter the choice : "))
    if choice ==1:
        pass
    elif choice==2:
        kill_sess=DB()
        #kill_sess.print_arg_list()
        f_path_name="C:/Users/rpalanisamy/Documents/PyScript/logs/kill_DB_sessions.log"
        kill_sess.DefineLogger(f_path_name)
        arglist=kill_sess.setArgsList(sys.argv)
        kill_sess.MakeConnection(arglist[0],arglist[1],arglist[2],arglist[3],arglist[4])
        DB_session_info=kill_sess.exec_proc(arglist[5])
        '''
        if DB_session_info !=[]:
            kill_sess.Kill_DB_sessions(DB_session_info)
        '''
