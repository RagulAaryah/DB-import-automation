from paramiko import SSHClient
import sys,logging,os,cx_Oracle

if __name__=="__main__":
    # Create and configure logger
    logging.basicConfig(filename="C:/Users/rpalanisamy/Documents/PyScript/logs/Stop_WM_MDA_MIP.log",
					format='%(asctime)s %(message)s',
					filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    try:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
        arglist=sys.argv[1:]
    except:
        logger.error("Arguements passed is invalid , try again !")

    #creating an instance of SSH
    client = SSHClient()
    
    #establishing a connection to the host 
    try:
        client.connect(str(arglist[0]),username=str(arglist[1]), password=str(arglist[2]))
        logger.info("connection established successfully!!")
    except:
        logger.error("connection failed due to invalid credentials")
        print("connection failed !")
    
    #connecting to sql plus 
    try:
        conn_str = 'import_export/impexpus3r/orclpdb'
        conn = cx_Oracle.connect(conn_str)
        c = conn.cursor()
        logger.info("connected to sql successfully")
    except:
        logger.error("connection failed , attempt again ")
    
    #try to fetch the SIDs to kill the active DB sessions
    try:
        SIDs=list(c.execute("SELECT SID FROM V$Session WHERE Status='ACTIVE' AND UserName IS NOT NULL;"))
        logger.info(" successfully fetched SIDs ")
        print("fetched SIDs successfully ")
    except:
        logger.error("failed to fetch the SIDs")
        print("fetching SIDs failed !")
    #attempting to the sessions using the fetched SIDs
    try:
        i=0
        while i<len(SIDs):
            pass
    except:
        pass