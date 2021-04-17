import pexpect
import time
import sys
import os
import re
from os import path



class RebootUccxServer:


    def Ping(self,server):
        pattern = r"win"
        windows = re.search(pattern, sys.platform)
        command = ("ping -n 6 "+str(server)) if windows else ("ping -c 6 "+str(server))
        resp = os.system(command)
        return (True if(resp == 0) else False)

    def execute(self,hostname,username,password):
        
        reboot_check={"status":None,"message":None}

        try:
            if self.Ping(hostname):
                msg = f"INFO Server {hostname} is up.."
                print (msg)

            else:
                msg = f"ERROR Server {hostname} is not up or reachable. "
                print(msg)
                reboot_check['status']=False
                reboot_check['message']=msg
                return reboot_check

            #Starting SSH session
            child = pexpect.spawn(f'ssh {username}@{hostname}')
            child.logfile_read = sys.stdout.buffer
            child.timeout = 4000

            child.expect('.*password:')
            child.sendline(f'{password}\n')
            check = child.expect(['.admin:', "denied", "password", pexpect.EOF, pexpect.TIMEOUT], timeout=65)

            if check != 0:
                msg = f"ERROR Authentication Failed for {self.username} on {hostname}"
                print(msg)
                reboot_check['status']=False
                reboot_check['message']=msg
                return reboot_check

            msg = f"INFO Logged in to the server {hostname} with {username}"
            print(msg)
            print("INFO Rebooting the Server")

            #initiating the reboot
            child.sendline("utils system restart\n")
            check = child.expect(["no\) ?", pexpect.EOF, pexpect.TIMEOUT], timeout=25)

            if check == 0:
                child.sendline("yes\n")
                time.sleep(20)
                child.close(force=True)
                
                reboot_check['status']=True
                reboot_check['message']="Reboot Initiated Successfully"
                return reboot_check
            else:
                child.close(force=True)
                reboot_check['status']=False
                reboot_check['message']="ERROR Reboot Initiation Failed"
                return reboot_check

        except Exception as e:
            msg = f"ERROR Could not Reboot the server {hostname}"
            print(msg)
            reboot_check['status']=False
            reboot_check['message']=str(e)
            return reboot_check


if __name__=="__main__":
    obj=RebootUccxServer()
    reboot_dict=obj.execute("hostname","username","password")
    print(reboot_dict)


