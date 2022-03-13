import paramiko as p
import yaml
#from subprocess import stdout

def send_command(host, username, password): 
   ssh = p.SSHClient() 
   ssh.set_missing_host_key_policy(p.AutoAddPolicy())
   ssh.connect(ip,port,user,password,timeout=5)
   stdin, stdout, stderr = ssh.exec_command("df")
   outline = stdout.readlines()
   resp = ''.join(outline)
   print(resp)
   ssh.close()

def get_config(config):
    print("Getting SSH credential...")
    _config = yaml.load(config)
    for key, value in _config.items(): 
        print(key + "  " + str(value))



def main():
    #   This is main 
    config_file = open("../ssh_config.yaml",'r')
    get_config(config_file)
    #send_command()
    print("Just a print for now")

if __name__ == "__main__":
    main()