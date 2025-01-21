

from msilib.schema import Error
import pysftp,sys,logging


if __name__=="__main__":
    
    # Create and configure logger
    logging.basicConfig(filename="C:/Users/rpalanisamy/Documents/PyScript/logs/SFTP_logs.log",
					format='%(asctime)s %(message)s',
					filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    #getting arguements from the command line 
    '''Those arguemtnts would be username, password , client folder , remaining path , filename and the local path'''
    try:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
        arglist=sys.argv[:7]
    except Exception as e:
        logger.error("Arguements passed is invalid , cause "+str(e))

    try:
        with pysftp.Connection('maftp.thruinc.net',port=22, username=arglist[1], password=arglist[2]) as sftp:#establishing the connection
            logger.info("connection established successfully !!")
            try:        
                with sftp.cd('/COMMON/ToManh/'): 
                    sftp.cd(str(arglist[3]))                                                          #this changes the directory to client folder 
                    sftp.cd(str(arglist[4]))                                                          # changing directory to the remaining path.
                    file="/COMMON/ToManh/"+str(arglist[3])+str(arglist[4])+str(arglist[5])
                    try:
                        sftp.get(str(arglist[5]),localpath=str(arglist[6]))                                    # get a remote file
                        logger.info("downloading was successful!")
                        print("download successful ")
                    except Exception as e:
                        logging.critical("download is unsuccessful due to the issue : "+str(e) )
                        print("Download failed !")
                        sys.exit(-1)
            except:
                sys.exit(-1)
    except Exception as e:
        logger.error("connection failed ! , cause :"+str(e))       


    