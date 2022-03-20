from asyncio.log import logger
from asyncore import file_dispatcher
from distutils.command.config import config
from genericpath import exists
from os import lseek
import paramiko as p
import yaml
import sys 
import logging 

class ssh_instance: 
    config_file = {}
    yaml_loc = "../ssh_config.yaml"
    def __init__(self, argv):
        logging.basicConfig(filename='../logging/ssh_script.log', format='%(asctime)s %(message)s',level=logging.DEBUG)
        #   To cut down on BS paramiko logs 
        logging.debug("Opening Config File")
        #   grab config and return into a dictionary 
        ssh_instance.config_file = self.get_config()
        print("printing config file\t\t")
        print(ssh_instance.config_file)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        if(len(sys.argv) > 1):
            self.check_flags(argv)
        #self.send_command(yaml_dict['host'], yaml_dict['user'], yaml_dict['password'])

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
    def get_config(self):
        logger.info("Getting SSH credentials...")
        config = open(self.yaml_loc,'r')
        _config = yaml.safe_load(config)
        print(_config)
        return _config
    '''
    #   Description: Checks incoming flags and calls respective function 
    #   Returns:     Nothing 
    '''
    def check_flags(self, argv):
        if sys.argv[1] == "-c":
            print(5)
            self.change_credentials()
            print(6)
            return 
        else: 
            logging.warn("Invalid flag, Aborting program")
        print(7)
    '''
    #   Description: Changes SSH credentials   
    #   Returns:     Nothing 
    '''
    def change_credentials(self):
        logger.info("Time to change SSH Credentials")
        username = ""
        _password = ""
        print(1)
        while len(username) == 0: 
            username = input("Enter Username\n")
            if len(username) == 0: 
                print("Enter a username!\n")
        print("\n\n")
        print(2)
        while len(_password) == 0: 
            _password = input("Enter Password\n")
            if len(_password) == 0: 
                print("Enter a password!\n")
        print(3)
        self.save_yaml(username,_password)
        #logging.info("Username and Password changed")
        
    def save_yaml(self,username,password): 
        print(4)
        #print("this is the old config " + self.config_file)
        self.config_file["user"] = username
        self.config_file["password"] = password
        #print(self.config_file)
        with open(self.yaml_loc, 'w') as f: 
            yaml.dump(self.config_file,f)
        
def main(argv):
    test = ssh_instance (argv)



if __name__ == "__main__":
    main(sys.argv)