import paramiko as p
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


def main():
    #   This is main 
    send_command()
    print("Just a print for now")

if __name__ == "__main__":
    main()