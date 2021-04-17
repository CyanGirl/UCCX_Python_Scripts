import pexpect
import time
import sys
import getpass
import os
import re

class CheckHostType:
    
    
    def checkHostType(self,output):
        splitted=output.split("\n")
        splitted=[temp for temp in splitted if "Primary Node" in temp]
        node=splitted[0].split("=")[1]
        print(node)

        if "true" in node.lower():
            print("Primary")
            self.logwrite(f"INFO Primary Server Detected.")
            return "Primary"
        else:
            print("Secondary")
            self.logwrite(f"INFO Secondary Server Detected.")
            return "Secondary"

    def execute(self,hostname,username,password):
        
        try:
        
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
                return msg

            msg = f"INFO Logged in to the server {hostname} with {username}"
            print(msg)

            #taking service list
            child.sendline("utils service list\n")
            time.sleep(8)
            check=child.expect(['.admin:',pexpect.EOF, pexpect.TIMEOUT],timeout=50)
            output=child.before.decode()

            if check!=0:
                msg=f"ERROR Command -utils service list-could not be executed"
                child.close(force=True)
                return msg
            
            node=self.checkHostType(output)
            child.close(force=True)
            
            return node
        
        except Exception as e:
            return str(e)


if __name__=="__main__":
    obj=CheckHostType()
    node= obj.execute("hostname","username","password")
    print (node)
    
    
    