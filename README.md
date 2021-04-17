# UCCX Server Maintenance Scripts

---

<br>

## Requirements :

- Language : Python 3
- Library : Pexpect
- Base OS : Linux
- Remote UCCX : Hostname, Username, Password

---

<br>

## Description:

> These Scripts can be utilized to remotely connect to an UCCX Server over SSH session and execute commands on it. For this, the script should be executed from a Linux Base machine which has RSA key of the remote UCCX server, saved in it.

<br>

---

<br>

## Scripts in here :

<br>

> ### 1 . Check_Host_Type.py
>
> > **Inputs** : Hostname, Username, Password
> > <br><br> >> **Output** :
> >
> > - Node type of the UCCX server. Can be Primary or Secondary.
> > - In case of any error occured, that Error will be returned.

<br>

> ### 2 . Cpu_Utilisation.py
>
> > **Inputs** : Hostname, Username, Password
> > <br><br> >> **Output** : A dictionary is returned
> >
> > - It contains CPU Utilization percentage on the UCCX server
> > - The Process Load on the UCCX server.
> > - Errors if any occured
> > - The default value of all the three keys are None.

<br>

> ### 3 . Reboot_UCCX.py
>
> > **Inputs** : Hostname, Username, Password
> > <br><br> > > **Output** : A dictionary is returned
> >
> > - It contains the message corresponding to execution.
> > - It contains status of the UCCX server reboot
> > - The status will be False when the Reboot is unsuccessful with the Error in the message.

<br>

> ### 4 . Auto_Start_Services.py
>
> > **Inputs** : Hostname, Username, Password
> > <br><br> > > **Output** : A dictionary is returned
> >
> > - It contains the list of services of UCCX Server in it which are started during the execution of the script.
> > - It also contains status of the execution. When False, it indicates the script failures
> > - When this list is empty and status is True, it denotes all services are running successfully
> > - The dictionary will also contain the Error if any occurs during the execution.

---
