from asyncio.log import logger
from asyncore import file_dispatcher
from genericpath import exists
from os import lseek
import paramiko as p
import yaml
import sys 
import logging 

class ssh_instance: 
    def __init__(self, argv):
        logging.basicConfig(filename='../logging/ssh_script.log', format='%(asctime)s %(message)s',level=logging.DEBUG)
        #   To cut down on BS paramiko logs 
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        if len(sys.argv) > 2:
            logging.debug("Too many arguments")
            sys.exit()
        logging.debug("Opening Config File")
        config_file = open("../ssh_config.yaml",'r')
        #   grab config and return into a dictionary 
        yaml_dict = self.get_config(config_file)  
        self.send_command(yaml_dict['host'], yaml_dict['user'], yaml_dict['password'])

    
    '''
    #   Description: Sends bash command to machine via ssh 
    #   Returns:     Nothing 
    '''
    def send_command(self, host, username, password): 
        worked = True 
        try: 
            ssh = p.SSHClient() 
            ssh.set_missing_host_key_policy(p.AutoAddPolicy())
            ssh.connect(host,22,username,password,timeout=5)
            stdin, stdout, stderr = ssh.exec_command("df")
            outline = stdout.readlines()
            resp = ''.join(outline)
            logging.debug(resp)
            ssh.close()
        except: 
            worked = False
            logger.warn("Error found, check credentials")
        if worked: 
            logger.info("SSH Command sent successfully")
        
    '''
    #   Description: Retrieves credentials from yaml file  
    #   Returns:     Nothing 
    '''
    def get_config(self, config):
        logger.info("Getting SSH credentials...")
        _config = yaml.safe_load(config)
        return _config
        
def main(argv):
    test = ssh_instance (argv)


if __name__ == "__main__":
    main(sys.argv)