
import cx_Oracle,sys,logging


if __name__=="__main__":
# Create and configure logger
    logging.basicConfig(filename="C:/Users/rpalanisamy/Documents/PyScript/logs/kill_DB_sessions.log",
					format='%(asctime)s %(message)s',
					filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    #logging.getLogger("paramiko").setLevel(logging.DEBUG) 

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    try:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Arguments List:', str(sys.argv))
        logger.info(str('Arguments List : '+str(sys.argv)))
        arglist=sys.argv[1:]

    except:
        print("invalid arguements ")
        logger.info("arguements invalid ")
        sys.exit(-1)

    #making a DB connection
    try:
        #conn_str=dbuser+"/"+dbpassword+"@"+dbhostname+":"+dbport+"/"+dbservicename
        conn_str=arglist[0]+"/"+arglist[1]+"@"+arglist[2]+":"+arglist[3]+"/"+arglist[4]
        print("connection string : "+conn_str)
        DB_con=cx_Oracle.connect(conn_str)
        curs=DB_con.cursor()
        if curs is not None:
            print("DB connection is successful !")
            logger.info("DB connection is successful !")
        else:
            print("connection failed")
            print("DB version : "+DB_con.version)
            logger.info("DB version : "+DB_con.version)
            #print("DB connection successful !!")
            
    except: 
        logger.error("connection failed either due to server issues or the entered credential is invalid ! ")
        print("DB connection failed ! ")
        sys.exit(-1)
        
    try:
                                                                                #con.autocommit = True
                                                                                # Inserting a record into table employeeS
                                                                                #curs.execute("set serveroutput on")
        curs.callproc(arglist[5])                                               #set serveroutput on; 
        
                                                                                    #print("DB second script! ")
                                                                                    #for i in 
                                                                                    #curs.execute("ALTER SYSTEM KILL SESSION 'SID,SERIAL#' IMMEDIATE;")
                                                                                    #curs.execute("SELECT SID, Serial#, UserName, Status, SchemaName, Logon_Time FROM V$Session WHERE Status='ACTIVE' AND UserName IS NOT NULL; ")
        try:
            print("trying to print the query")
            a=curs.fetchall()
            if not a:
                print("rows empty")
                logger.info("rows empty")
            else:
                for rows in a :
                    print(rows)
                print("it's done !")
        except cx_Oracle.Error as e:
            print("unable to print the query output")
            logger.error(e)     
                                                                                    #print(output)
                                                                                    # commit() to make changes reflect in the database
                                                                                    #DB_con.commit()
                                                                                    #logging.info(str(output))
    except cx_Oracle.Error as e:
        print(str(e))
        logger.error("cx_Oracle error : "+str(e))
    except cx_Oracle.DatabaseError as e:
        print("There is a problem with Oracle "+str(e))
        logger.error("cx_Oracle DataBaseError "+e)
    except:
        print("error in the execution of the query ")
        logger.error("error in the execution of the query #userdefined log , error not exactly known")
    
     
