from asyncore import file_dispatcher
from genericpath import exists
from os import lseek
import paramiko as p
import yaml
import sys 

class ssh_instance: 
    def __init__(self, incoming_state):
        ssh_instance.state = incoming_state 
        ssh_instance.print_state(self)
        if len(sys.argv) > 2:
            print("Too many arguments")
            sys.exit()
        config_file = open("../ssh_config.yaml",'r')
        #   open file for logging 
        log_file = self.start_log()
        #   grab config and return into a dictionary 
        yaml_dict = self.get_config(config_file)  
        self.send_command(yaml_dict['host'], yaml_dict['user'], yaml_dict['password'])

    def print_state(self):
        print(self.state)
    '''
    #   Description: Sends bash command to machine via ssh 
    #   Returns:     Nothing 
    '''
    def send_command(self, host, username, password): 
        ssh = p.SSHClient() 
        ssh.set_missing_host_key_policy(p.AutoAddPolicy())
        ssh.connect(host,22,username,password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command("df")
        outline = stdout.readlines()
        resp = ''.join(outline)
        print(resp)
        ssh.close()
    '''
    #   Description: Retrieves credentials from yaml file  
    #   Returns:     Nothing 
    '''
    def get_config(self, config):
        print("Getting SSH credential...")
        _config = yaml.load(config)
        return _config
    '''
    #    Description: Opens file for logging, creates file if file doesn't exist 
    #    Returns:     File object for logging
    '''
    def start_log(self): 
        filepath = "../logging/ssh_script_log.txt"
        file=''
        if exists(filepath):
            print("File exists.. Starting Log. \n")
            file = open(filepath,"a+")
        else: 
            print("File doesn't exist.. Creating file. Starting Log\n")
            file = open(filepath, "w+")
        return file 
    
    


def main(argv):
    test = ssh_instance ("test")


if __name__ == "__main__":
    main(sys.argv)