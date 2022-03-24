from asyncio.log import logger
from asyncore import file_dispatcher
from distutils.command.config import config
from genericpath import exists
from os import lseek
import paramiko as p
from paramiko import HostKeys
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
        # print("printing config file\t\t")
        # print(ssh_instance.config_file)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        if(len(sys.argv) > 1):
            self.check_flags(argv)
        self.send_command(self.config_file['hostname'], self.config_file['username'], self.config_file['password'])

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
            command = "ls; df -h"
            stdin, stdout, stderr = ssh.exec_command(command)
            outline = stdout.readlines()
            resp = ''.join(outline)
            logging.debug(resp)
            print(resp)
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
            self.change_credentials()
            return 
        if sys.argv[1] == "-h":
            self.change_hostname() 
            return
        else: 
            logging.warn("Invalid flag, Aborting program")

    '''
    #   Description: Changes SSH credentials   
    #   Returns:     Nothing 
    '''
    def change_credentials(self):
        logger.info("Time to change SSH Credentials")
        username = ""
        _password = ""
        while len(username) == 0: 
            username = input("Enter Username\n")
            if len(username) == 0: 
                print("Enter a username!\n")
        print("\n")
        self.save_yaml("user",_password)
        while len(_password) == 0: 
            _password = input("Enter Password: ")
            if len(_password) == 0: 
                print("Enter a password!\n")
        self.save_yaml("password",_password)
        logging.info("Username and Password changed")
        user_in = input("Run saved command?\t")
        if user_in != "yes":
            print("Okay, exiting\n")
            sys.exit() 
    '''
    #   Description: Changes host IP address  
    #   Returns:     Nothing 
    '''
    def change_hostname(self): 
        logging.info("Changing host IP address")
        _host = ""
        while len(_host) == 0: 
            _host = input("Enter IP address: ")
            if len(_host) == 0: 
                print("Enter new IP address!")
        self.save_yaml("hostname", _host)
        logging.info("Changed hostanme")
        user_in = input("Run saved command?\t")
        if user_in != "yes":
            print("Okay, exiting\n")
            sys.exit() 
        
    '''
    #   Description: Saves dictionary changes to yaml file    
    #   Returns:     Nothing 
    '''
    def save_yaml(self ,_key, _newVal): 
        self.config_file[_key] = _newVal
        with open(self.yaml_loc, 'w') as f: 
            yaml.dump(self.config_file,f)
        
def main(argv):
    test = ssh_instance (argv)



if __name__ == "__main__":
    main(sys.argv)