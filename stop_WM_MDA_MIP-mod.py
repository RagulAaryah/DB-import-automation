from paramiko import SSHClient
import sys,logging,os,paramiko
class Error(Exception):
    """Base class for other exceptions"""
    pass

class PathInvalidError(Error):
    """Raised when the path is invalid """
    pass
class FileDoesntExistError(Error):
    """raised when file doesn't exist"""
    pass

if __name__=="__main__":
    # Create and configure logger
    logging.basicConfig(filename="C:/Users/rpalanisamy/Documents/PyScript/logs/Stop_WM_MDA_MIP.log",
					format='%(asctime)s %(message)s',
					filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    logging.getLogger("paramiko").setLevel(logging.DEBUG) 
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    try:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
        arglist=sys.argv[1:]
    except:
        logger.error("Arguements passed is invalid , try again !")

    #creating an instance of client
    client = SSHClient()
    #establishing a connection 
    try:
        #client.connect(str(hostname=arglist[0]).strip(),username="wmsadmin",port=22, password="wmsadmin")
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=arglist[0],username='wmsadmin',password='wmsadmin')
        print("connection successful")
        channel = client.invoke_shell()
        channel.send(' -a\n' )

        buff=''
        while not buff.endswith('# '): # Checking for returned prompt
            logging.info("inside while block")
            resp = channel.recv(4096)
            buff += resp
            print(resp)
        print("connection established!")
        logger.info("connection established successfully!!")
    except:    
        logger.error("connection failed due to unexpected error ")
        sys.exit(-1)
        
    try:
        path= "/apps/scope/products/WM/tools/bin"
        if (os.path.isdir(path)==False):
            logging.critical("Entered path is not valid !")
            raise PathInvalidError
        else:
            stdin, out, err = client.exec_command(str("cd "+path))
            print("stdout: " + out.read())
            logging.info("path switched to "+path)
    except PathInvalidError:
        print("the entered path is invalid ")
    except:
        logger.error("error in execution of the command ")

    #trying to execute the stop WM schema commmand
    try:
        if os.path.isfile(arglist[1])==False:
            raise FileDoesntExistError
        try:
            stdin, out, err = client.exec_command(str("./"+str(arglist[1]+" stop wms")))
            print("stdout: " + out.read())
            logging.info("stopped WM/MDA/MIP schemas !")
        except:
            logging.error("error while executing the stop script")

    except FileDoesntExistError:
        logging.error(f"{arglist[1]} doesn't exist.")
        print(f"{arglist[1]} not found ")      

    
        
    
    client.close()