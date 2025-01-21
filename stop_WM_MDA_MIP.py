from paramiko import SSHClient
import sys,logging,os
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
    #establishing a connection 
    try:
        client.connect(hostname=arglist[0],username='wmsadmin',password='wmsadmin')
        logger.info("connection established successfully!!")
    except:    
        logger.error("connection failed ")
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
        if os.path.isfile(arglist[3])==False:
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