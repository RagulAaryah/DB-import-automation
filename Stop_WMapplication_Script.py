
from paramiko import SSHClient
import sys,logging,paramiko



if __name__=="__main__":
    # Create and configure logger
    logging.basicConfig(filename="C:/Users/rpalanisamy/Documents/PyScript/logs/Stop_WM.log",
					format='%(asctime)s %(message)s',
					filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    #logging.getLogger("paramiko").setLevel(logging.DEBUG) 

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.INFO)
    try:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Arguments List:', str(sys.argv))
        #logging.info(str('Number of arguments:'+str(len(sys.argv))+ ' arguments.'))
        logging.info(str('Arguments List : '+str(sys.argv)))
        arglist=sys.argv[1:]
        #logging.info("1.The Hostname : "+str(arglist[0]))
        #logging.info("The script invoked : "+str(arglist[1]))
    except:
        logger.error("Arguements passed is invalid , try again !")
        sys.exit(-1)

    #creating an instance of client
    client = SSHClient()
    #establishing a connection 
    try:
        #client.connect(str(hostname=arglist[0]).strip(),username="wmsadmin",port=22, password="wmsadmin")
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=arglist[0],username='wmsadmin',password='wmsadmin')
        print("Successfully logged into the Host : "+arglist[0]+"  !")
        logger.info("Successfully logged into the Host : "+arglist[0]+"  !")
    except:    
        logger.error("connection failed due to unexpected error ")
        client.close()
        sys.exit(-1)
    
    try:
        command_string= 'cd /apps/scope/products/WM/tools/bin;'+"sh "+arglist[1]+" stop wms"
        #print(command_string)
        #channel = client.get_transport().open_session()
        #channel.exec_command('cd /apps/scope/products/WM/tools/bin')
        #stdin, stdout, stderr = channel.exec_command('cd /apps/scope/products/WM/tools/bin')
        #b=str(stdout.read())
        #stop="./"+arglist[1]+" stop wms"
        #(stdin,stdout, stderr) = client.exec_command(command_string)
        (stdin,stdout, stderr) = client.exec_command('cd /apps/scope/products/WM/tools/bin; bash '+arglist[1]+' stop wms')
        a=str(stderr.read())
        if a=="b''":
            logging.info("status : Successfully shutdown WM application !")
            print("status : Successfully shutdown WM application !")
        else:
            logging.info("Error during execution , cause : "+a) 

    except:
        logger.error("error in execution of the cd ")
        client.close()
        sys.exit(-1)

        
    
    client.close()