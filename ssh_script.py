from os import lseek
import paramiko as p
import yaml
import sys 

class ssh_instance: 
    def __init__(self, incoming_state):
       ssh_instance.state = incoming_state 
       ssh_instance.print_state(self)
    def print_state(self):
        print(self.state)
    ##############################################################
    #   Description: Sends bash command to machine via ssh 
    #   Returns:     Nothing 
    ##############################################################
    def send_command(host, username, password): 
        ssh = p.SSHClient() 
        ssh.set_missing_host_key_policy(p.AutoAddPolicy())
        ssh.connect(ip,port,user,password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command("df")
        outline = stdout.readlines()
        resp = ''.join(outline)
        print(resp)
        ssh.close()






##############################################################
#   Description: Sends bash command to machine via ssh 
#   Returns:     Nothing 
##############################################################
def send_command(host, username, password): 
   ssh = p.SSHClient() 
   ssh.set_missing_host_key_policy(p.AutoAddPolicy())
   ssh.connect(ip,port,user,password,timeout=5)
   stdin, stdout, stderr = ssh.exec_command("df")
   outline = stdout.readlines()
   resp = ''.join(outline)
   print(resp)
   ssh.close()


##############################################################
#   Description: Retrieves credentials from yaml file  
#   Returns:     Nothing 
############################################################## 
def get_config(config):
    print("Getting SSH credential...")
    _config = yaml.load(config)
    return _config



def main(argv):
    test = ssh_instance ("test")
    if len(sys.argv) > 2:
        print("Too many arguments")
        sys.exit()
    config_file = open("../ssh_config.yaml",'r')
    #   grab config and return into a dictionary 
    yaml_dict = get_config(config_file)     
    #   for testing.. 
    print(yaml_dict['states'])
    
    #send_command()
    print("Just a print for now")

if __name__ == "__main__":
    main(sys.argv)