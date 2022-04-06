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
from hashlib import sha256 #    For password hashing 

class ssh_instance: 
    config_file = {}
    yaml_loc = "../ssh_config.yaml"
    def __init__(self, argv):
        logging.basicConfig(filename='../logging/ssh_script.log', format='%(asctime)s %(message)s',level=logging.DEBUG)
        #   To cut down on BS paramiko logs 
        logging.debug("Opening Config File")
        #   grab config and return into a dictionary 
        ssh_instance.config_file = self.get_config()
        print (ssh_instance.config_file)
        print("\n")
        profile_list = list(ssh_instance.config_file["profiles"].keys())
        print(profile_list)
        #   check if password exists 
        # if "password" in self.config_file.keys(): 
        #     self.check_password()
        # else: 
        #     self.enter_password()
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        # if(len(sys.argv) > 1):
        #     self.check_flags(argv)
        #self.send_command(self.config_file['hostname'], self.config_file['username'], self.config_file['password'])

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
            logger.warning("Error found, check credentials")
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
        #print(_config)
        return _config
    '''
    #   Description: Checks incoming flags and calls respective function 
    #   Returns:     Nothing 
    '''
    def check_flags(self, argv):
        _argv = sys.argv[1]
        if _argv == "-a": 
            self.add_command()
        if _argv == "-c":
            self.change_credentials()
            return 
        if _argv == "-h":
            self.change_hostname() 
            return
        if _argv == "-t": #   for test
            print("testing for now... ")
            return
        if _argv == "--add_host":
            self.add_host()
        else: 
            logging.warning("Invalid flag, Aborting program")

    '''
    #   Description: Changes SSH credentials   
    #   Returns:     Nothing 
    '''
    def change_credentials(self):
        logger.info("Time to change SSH Credentials")
        username = ""
        _password = ""
        self.check_user_input(username)
        self.save_yaml("user",_password)
        self.check_user_input(_password)
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
        self.check_user_input(_host)
        self.save_yaml("hostname", _host)
        logging.info("Changed hostanme")
        user_in = input("Run saved command?\t")
        if user_in != "yes":
            print("Okay, exiting\n")
            sys.exit() 
        
    '''
    #   Description: Adds Host to yaml     
    #   Returns:     Nothing 
    '''
    def add_host(self): 
        logging.debug("Adding host")
        _hostname = input("Enter nickname of host\n")
        _user = input("Enter Username: \n")
        _password = input("Enter password\n")
        this_list = [_user, _password]
        self.save_yaml("host_"+_hostname, this_list)

    '''
    #   Description: Saves dictionary changes to yaml file    
    #   Returns:     Nothing 
    '''
    def save_yaml(self ,_key, _newVal): 
        self.config_file[_key] = _newVal
        with open(self.yaml_loc, 'w') as f: 
            yaml.dump(self.config_file,f)
    
    def check_user_input(self,value): 
        while len(value) == 0: 
            _value = input("Enter IP address: ")
            if len(value) == 0: 
                print("Enter new IP address!")
    '''
    #   Description: Checks if user entered password matches hashed password in yaml  
    #   Returns:     Nothing 
    '''
    #   Gonna wait on this 
    # def check_password(self):
    #     yamlpass = self.config_file["password"] 
    #     _input = input("Enter your password\n")
    #     userpass = sha256(_input.encode('utf-8')).hexdigest()
    #     if yamlpass != userpass: 
    #         logging.warning("Incorrect password, exiting\n")
    #         sys.exit()
    # '''
    # #   Description: No password detected, user creates password 
    # #   Returns:     Nothing 
    # '''
    # def enter_password(self):
    #     logging.info("No password found in config, let's create one now\n")
    #     _input = input("Enter your password\n")
    #     emp_str = ""
    #     while emp_str != "yes" : 
    #         emp_str = input("You entered.. " + _input + "\t Enter yes if that is your password.")
    #         if emp_str != "yes": 
    #             _input = input("Enter password\n")
    #     new_pass = sha256(_input.encode('utf-8')).hexdigest()
    #     self.save_yaml("password", new_pass)
        
def main(argv):
    test = ssh_instance (argv)



if __name__ == "__main__":
    main(sys.argv)