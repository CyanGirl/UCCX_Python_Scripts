import pexpect
import time
import sys
import os
import re

class CpuUtilization:

    #method to extract Cpu utilization percentage
    def processCpu(self,output):

        output=output.split("\n")
        pattern="CPU Idle:"
        find=[temp for temp in output if re.search(pattern,temp)][0]
        find=[temp for temp in find.split(" ") if temp!=""]
        percentage=round(100-(float(find[2][0:-1])),3)
        return percentage

    #method to process the SSH session
    def execute(self,hostname,username,password):
        
        cpu_output={"cpu_utilization":None,"process_load":None,"error":None}

        try:
            #SSH session
            child = pexpect.spawn(f'ssh {username}@{hostname}')
            child.logfile_read = sys.stdout.buffer
            child.timeout = 700
            
            child.expect('.*password:')
            child.sendline(f'{password}\n')
            check=child.expect(['.admin:',"denied","password",pexpect.EOF, pexpect.TIMEOUT],timeout=65)
            if check!=0:
                msg=f"ERROR Authentication Failed for {username} on {hostname}"
                cpu_output['error']=msg
                child.close(force=True)
                return cpu_output

            #To get the CPU utilization
            child.sendline('show status\n')
            check=child.expect(['.admin:',pexpect.EOF, pexpect.TIMEOUT],timeout=20)
            output=child.before.decode()
            if check!=0:
                msg=f"ERROR Command-show status- could not be executed"
                cpu_output['error']=msg
                child.close(force=True)
                return cpu_output
            percentage=self.processCpu(output) 
            cpu_output['cpu_utilization']=percentage
            
            #to get the process load
            child.sendline("show process load cpu\n")
            check=child.expect(['.admin:',pexpect.EOF, pexpect.TIMEOUT],timeout=25)
            output=child.before.decode()
            if check!=0:
                msg=f"ERROR Command-process load- could not be executed for {hostname}"
                cpu_output['error']=msg
                child.close(force=True)
                return cpu_output
            cpu_output['process_load']=output
            
            #killing the child process
            child.close(force=True)
            return cpu_output

        #in case of any exception
        except Exception as e:
            cpu_output['error']=str(e)
            return cpu_output

        
if __name__=="__main__":
    obj=CpuUtilization()
    Cpu_Dict=obj.execute("host1","test123","test123@")
    print(Cpu_Dict)


