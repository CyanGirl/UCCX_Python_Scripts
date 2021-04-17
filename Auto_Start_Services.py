import os
import pexpect
import time
import sys
import re



class AutostartService:
    
    
    def Ping(self,server):
        pattern = r"win"
        windows = re.search(pattern, sys.platform)
        command = ("ping -n 6 "+str(server)) if windows else ("ping -c 6 "+str(server))
        resp = os.system(command)
        return (True if(resp == 0) else False)

    def processList(self,output):

        output=output.split("\n")
        pattern=r'[STOPPED]'
        find=[temp for temp in output if pattern in temp]
        stoppedList=list(map(lambda name:name.split("[")[0].strip(),find))
        if os.path.exists(f"{self.inputpath}TrackService.json"):
            self.processJson(stoppedList)
        return(stoppedList)

    def execute(self,hostname,username,password):
        
        services_started={"services":[],"status":None,"error":None}

        try:
            
            if self.Ping(hostname):
                msg = f"INFO Server {hostname} is up.."
                print (msg)

            else:
                msg = f"ERROR Server {hostname} is not up or reachable. "
                print(msg)
                services_started['status']=False
                services_started['error']=msg
                return services_started

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
                services_started['status']=False
                services_started['error']=msg
                return services_started

            msg = f"INFO Logged in to the server {hostname} with {username}"
            print(msg)

            #taking out stopped services
            child.sendline("utils service list\n")
            time.sleep(8)
            check=child.expect(['.admin:',pexpect.EOF, pexpect.TIMEOUT],timeout=50)
            output=child.before.decode()

            if check!=0:
                msg=f"ERROR Command -utils service list-could not be executed"
                child.close(force=True)
                services_started['status']=False
                services_started['error']=msg
                return services_started

            serviceList=self.processList(output)
            
            #service list ;data type=array
            print(serviceList)

            if len(serviceList)<1:

                msg="INFO All Services are running successfully"
                print(msg)
                services_started['status']=True

            else:
                
                restarted=[]
                for service in serviceList :
                    
                    msg=f"INFO Starting {service} Initiated"
                    print(msg)
                    child.sendline(f"utils service start {service}\n")
                    time.sleep(5)
                    check=child.expect(['.admin:',pexpect.EOF, pexpect.TIMEOUT],timeout=300)
                    output=child.before.decode()  

                    #send mail for restarted
                    if "STARTED" in output:
                        msg=f"INFO {service} Started Successfully"
                        print(msg)
                        restarted.append(service)

                    elif "STARTED" not in output:
                        msg=f"ERROR {service} Start Has Failed"
                        self.logwrite(msg)
                        self.writeJson(service)
   
                print("INFO Closing the session..")
                child.close(force=True)

        except Exception as e:
            print(e)
            child.close(force=True)
            services_started['status']=False
            services_started['error']=str(e)
            return services_started

if __name__=="__main__":
    obj=AutostartService()
    service_dict=obj.execute("hostname","username","password")
    print(service_dict)      
        

