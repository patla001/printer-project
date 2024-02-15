#/bin/python
''' 
=== Name: pySetupPrinter.py
=== Description: 
    The Python script is design for friendly user testing on Mobile App for the Android or iOS Mobile.
=== Outline:
    1) OOBE reset 
    2) Change Persona
       a) Traditional or loyal
    3) Change Stack
       a) Stage, PIE, and Production (PP)
    4) Check/Set if is Permanent UCDE Dev Mode
    5) View the current SKU Configuration 
    
=== Install Libraries example:
    python -m pip install paramiko
    
=== Author: 
    Ezer Patlan-Almeida
    
=== Copyright:
    Copyright (c) 2023 
    
=== Version         Date            Comments
        1.01          05/17/2022      Created Script 
        1.02          09/19/2022      Error Prompt once is offline
        1.03          09/20/2022      Error Prompt once you exit the Python Script
        1.04          02/02/2023      Check/Set if the unit is Dev Mode
        1.05          02/27/2023      Check/Set the unit SKU
        1.06          05/19/2023      Correcting the Network Time out
        1.06          05/19/2023      Added Factory Reset 4
        1.06          05/19/2023      Check Persona and Stack
        1.06          05/19/2023      Refactor Check/Set for the unit SKU code
        1.06          05/19/2023      Device UUID is added 
        1.06          05/19/2023      Added Color Text in the Terminal Prompt 
        1.07          05/31/2023      Added Error Exception while printer is offline
        1.08          08/03/2023      Change the Stack to Production

'''

def installLibrary(packageName):
    import subprocess
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', packageName])

    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return installed_packages
    #print(installed_packages)

#try:
#import subprocess
import sys
import time
import enum
import argparse
import socket
import re


#print('paramiko' in sys.modules)
# try:
#     #if 'paramiko' in sys.modules == False:
#     import paramiko
    
# #else:
# except Exception as e:
#     packageName = 'paramiko'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)
#     import paramiko

# try:
#     import paramiko
    
# except ModuleNotFoundError as e:
#     packageName = 'paramiko'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)
#    # pass


try:
    import paramiko
    import requests
    import telnetlib
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


except ModuleNotFoundError as e:
    print("Error found: %s" % e)
    if re.search('paramiko',str(e)):
        packageName = 'paramiko'
        print("python -m pip install %s " % packageName)
        exit()
    elif re.search('requests', str(e)):
        packageName = 'requests'
        print("python -m pip install %s "% packageName)
        exit()
    elif re.search('telnetlib', str(e)):
        packageName = 'telnetlib'
        print("python -m pip install %s " % packageName)
        exit()
    elif re.search('urllib3', str(e)):
        packageName = 'urllib3'
        print("python -m pip install %s "% packageName)
        exit()
    else:
        pass
    #packageName = e[0]
    #install_packages = installLibrary(packageName)
    


# if 'paramiko' in sys.modules == False:
#     packageName = 'paramiko'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)

# if 'paramiko' in sys.modules == True:
#     import paramiko


# if 'requests' in sys.modules == False:
#     packageName = 'requests'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)

# if 'requests' in sys.modules == True:
#     import requests
    
# if 'telnetlib' in sys.modules == False:
#     packageName = 'telnetlib'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)

# if 'telnetlib' in sys.modules == True:
#     import telnetlib
    
# if 'urllib3' in sys.modules == False:
#     packageName = 'urllib3'
#     installed_packages = installLibrary(packageName)
#     print(installed_packages)

# if 'urllib3' in sys.modules == True:
#     import urllib3
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



#except Exception as e:
#    #print (e)
#    print("Error, missing libraries: {}".format(e))
    
    
#HOST = "15.1.192.74"
#HOST = "15.1.195.140"
#PORT = 9104
#HOST = sys.argv[1]
#PORT = sys.argv[2]
#TIMEOUT = 7


''' pseudo commands is a class with two inputs, str and enum.Enum. 
str represents the pseudo command line, and enum.Enum is the numberical 1, 2, and 3.'''
class pseudoCommand:
    oobeReset = ""
    reset4 = ""
    personaStatus = ""
    stackStatus = ""
    getModelName = ""
    getSerialNum = ""
    setFlex = ""
    setE2E = ""
    setStage = ""
    setPie = ""
    setProd = ""
    isDevMode = ""
    setDevMode = ""
    getSKUConfig = ""
    setSKUConfig = " "
    getCloudID = " "
    fin  = "!!!end!!! "



def execute(commands, tn):
   # str = cmd.encode('utf-8') + b"\r\n\r\n"
    cmd = " "
    str =  cmd.encode('utf-8') + b"\r\n\r\n"
    
    tn.write(str)
    for cmd in commands:
        #print(cmd)
        tn.write(cmd.encode('utf-8')+b"\r\n")
    
    outPrompt = tn.read_until((pseudoCommand.fin).encode('utf-8')+b"\r\n",timeout=3)
    
    return outPrompt



def execute5026(cmd, tn):
    str = cmd.encode('utf-8') + b"\n"
    retstr = b'udws() returns 0 (0x0)'
    tn.write(str)
    out = tn.read_until(retstr).decode('utf-8')
    return out

def editTelnet(HOST, PORT, TIMEOUT):
    #HOST = sys.argv[1]
    #PORT = sys.argv[2]
    #TIMEOUT = 7
    CDEFAULT = '\33[0m'
    CYELLOW = "\33[43m"
    CEND = "\033[0m"
    try:
        tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
        ''' this is for debuging 
        '''
        
        tn.interact();
        
    except socket.timeout:
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        title='\tConnection Failed/Time-out: Check your Network or IP Address\n'
        response=headerTile+title+headerTile
        sys.exit(response)
    except socket.error:
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        #title='\t\t\t\tConnection Closed\n'
        #response=headerTile+title+headerTile
        title=CDEFAULT + 'Device: ' + CEND + CYELLOW + ' Connection Closed! ' + CEND
        response=CYELLOW + title + CEND
        sys.exit(response)

    except ConnectionResetError:
        
        title=CDEFAULT + 'Device: ' + CEND + CYELLOW + ' Connection Closed! ' + CEND
        response=CYELLOW + title + CEND
        sys.exit(response)

def toDecode(step):
    out = step.decode("utf-8")
    #output = out.replace("\r\n", "\r")

    
    return out
    #return print(out)

def exportSerialNumber(HOST,PORT, TIMEOUT):
    #HOST = sys.argv[1]
    #PORT = sys.argv[2]
    #TIMEOUT = 7
    
    try: 
            tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
            pseudo = [pseudoCommand.getSerialNum];
            response = 'Connected'
    except socket.timeout:
            headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
            title='\tConnection Failed/Time-out: Check your Network or IP Address\n'
            response=headerTile+title+headerTile
            sys.exit(response)
    
    #tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
    #pseudo = [pseudoCommand.getSerialNum];
    
    cmd = " "
    str =  cmd.encode('utf-8') + b" "
    tn.write(str)
    for cmd in pseudo:
        tn.write(cmd.encode('utf-8')+b"\r")

    out = tn.read_until(("(mainApp:9104)> ").encode('utf-8')+b"\r",timeout=3)
    decodeOut = out.decode("utf-8")
    output = decodeOut.replace("\r\n", "\r")
    setOutput = output.split()
    return setOutput[-2]


def exportModelName(HOST,PORT, TIMEOUT):
    #HOST = sys.argv[1]
    #PORT = sys.argv[2]
    #TIMEOUT = 7
    
    try: 
            tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
            pseudo = [pseudoCommand.getModelName];
            response = 'Connected'
    except socket.timeout:
            headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
            title='\tConnection Failed/Time-out: Check your Network or IP Address\n'
            response=headerTile+title+headerTile
            sys.exit(response)
    
    #tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
    #pseudo = [pseudoCommand.getSerialNum];
    
    cmd = " "
    str =  cmd.encode('utf-8') + b" "
    tn.write(str)
    for cmd in pseudo:
        tn.write(cmd.encode('utf-8')+b"\r")

    out = tn.read_until(("(mainApp:9104)>").encode('utf-8')+b"\r",timeout=3)
    decodeOut = out.decode("utf-8")
    output = decodeOut.replace("\r\n", "\r")
    setOutput = output.split()
    nameOutput = []
    indexOutput = []
    for i in range(len(setOutput)):
        if '(mainApp:9104)>' == setOutput[i]:
            indexOutput = i
        if indexOutput:
            nameOutput.append(setOutput[i])
    
    
    print("Model Name Unit: ", end="")
        
    for i in range(len(nameOutput)):
        if '(mainApp:9104)>' != nameOutput[i]:
            print("{} ".format(nameOutput[i]),end="")
        
    print("\n")
    
    #return nameOutput

def exportInfo(HOST):
    try: 
        url = "https://" +  HOST + ""
        data = requests.get(url, verify=False)
        output = data.json()
        nameUnit = output['makeAndModel']['name']
        firmwareVersion = output['firmwareVersion']
        serialNumber = output['serialNumber']
        uuid =  output['deviceUuid']
        response = 'Connected'
        CGREEN = '\33[92m'
        CRED = "\33[93m"
        CBLINK = '\33[6m'
        CEND = "\33[0m"
        ThunderEmoji = "\U000026A1"
        print("Device: " + ThunderEmoji + CGREEN + response + CEND + ThunderEmoji);
        print(CRED + "Unit Name: ", nameUnit + CEND)
        print(CRED + "Current Firmware Version: ", firmwareVersion + CEND)
        print(CRED + "Serial Number: ", serialNumber + CEND)
        print(CRED + "UUID: ", uuid + CEND)
    except requests.exceptions.ConnectionError:
        CRED = "\33[93m"
        CBLINK = '\33[6m'
        CEND = "\33[0m"
        SleepyEmoji =  "\U0001F62A"
        printerStatus=  'Device: ' + SleepyEmoji + CBLINK + ' Disconnected ' + CEND + SleepyEmoji + '\n'
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        title='\t[~] BOOOM! Server has been exploded!\n' 
        response=printerStatus + CRED + headerTile+title+headerTile + CEND
        #response="Error sending data: %s" % e
        #print("Error sending data: %s" % e)
        sys.exit(response)

def checkSerialNumber(HOST, PORT, TIMEOUT):
    serialNumber = exportSerialNumber(HOST, PORT, TIMEOUT);
    
    if (serialNumber == "0000000010"):
        editTelnet()
    else:
        print("Serial Number: ", serialNumber)
    

def checkConnection(HOST,PORT,TIMEOUT):
    CGREEN = '\33[92m'
    CRED = '\33[91m'
    CBLINK = '\33[6m'
    CEND = '\33[0m'
    ThunderEmoji = "\U000026A1"
    SleepyEmoji =  "\U0001F62A"
    try:
        
        #HOST = sys.argv[1]
        #PORT = sys.argv[2]
        #TIMEOUT = 7 
        tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
        response = ' Connected '
    except socket.timeout as e:
        printerStatus=  'Device: ' + SleepyEmoji + CBLINK + ' Disconnected ' + CEND + SleepyEmoji + '\n'
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        title='\tConnection Failed: %s\n' % e 
        response=printerStatus + CRED + headerTile+title+headerTile + CEND
        #response="Error sending data: %s" % e
        #print("Error sending data: %s" % e)
        sys.exit(response)
        #sys.exit(1)
    except socket.gaierror as e:
        printerStatus=  'Device: ' + SleepyEmoji + CBLINK + ' Disconnected ' + CEND + SleepyEmoji + '\n'
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        title='\tConnection Failed: %s\n' % e
        response=printerStatus + CRED + headerTile+title+headerTile + CEND
        #response="Error sending data: %s" % e
        #print("Error sending data: %s" % e)
        #sys.exit(1)
        sys.exit(response)

    except socket.ConnectionError as e:
        printerStatus=  'Device: ' + SleepyEmoji + CBLINK + ' Disconnected ' + CEND + SleepyEmoji + '\n'
        headerTile='///////////////////////////////////////////////////////////////////////////////////\n'
        title='\tConnection Failed: %s\n' % e
        response=printerStatus + CRED + headerTile+title+headerTile + CEND
        #response="Error sending data: %s" % e
        #print("Error sending data: %s" % e)
        #sys.exit(1)
        sys.exit(response)

    except ConnectionResetError:
        CDEFAULT = '\33[0m'
        CYELLOW = "\33[43m"
        CEND = "\033[0m"
        title=CDEFAULT + 'Device: ' + CEND + CYELLOW + ' Connection Closed! ' + CEND
        response=CYELLOW + title + CEND
        sys.exit(response)


    except requests.exceptions.ConnectionError:
        print(' [~] BOOOM! Server has been exploded!')
        sys.exit(response)
        
    else:
       
        
        exportInfo(HOST)
    return tn


def ssh_command(router_ip, router_username, router_password, cmd, timeout):
    try:
        # Create a new SSHClient instance.
        ssh = paramiko.SSHClient()
        
        # Set connection timeout value.
        ssh.banner_timeout = timeout
        
        #Set host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to a remote server with a timeout .
        ssh.connect(router_ip, 22 , router_username, router_password, timeout=timeout)
        
        # Execute the command and return a list.
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True, timeout=timeout)
        
        # Get execution result, the readlines() method will return a list object.
        out = stdout.readlines()
        
        # Command execution status, 0 means success, 1 means fail.
        #channel = stdout.channel
        #status = channel.recv_exit_status()
        
        # Close ssh connection.
        ssh.close()
        
        # Modify the returned result object.
        #result['status'] = status
        #result['data'] = out
        
        # return result to outer invoker.
        return out
    except Exception as e:
        print (e)
        print("Error, connection to server or command execution timeout!! ip: {} command: {}".format(router_ip, cmd))
        return False

def sshFormat(executeCommand,flagPayload):

    if flagPayload == 0:
        
        part1 = "curl --silent --noproxy \'*\' -d"
        part2 = "\'{\"version\":\"1.0.0\",\"targetService\",\"mainApp\",\"blocking\":true,\"command\":\"" 
        part3 = executeCommand
        part4 = " \"}\' http://127.0.0.1/ | cut -f6 -d: | cut -f1 -d} | cut -f2 -d\\\" | base64 -d"
        cmd1 =  str(part1 + " " + part2 +  " " + part3 + " " + part4 ) 
        return cmd1

    if flagPayload == 1:

        payload = input("Type Payload/Hexadecimal/Decimal Number: ")
        part1 = "curl --silent --noproxy \'*\' -d"
        part2 = "\'{\"version\":\"1.0.0\",\"targetService\",\"mainApp\",\"blocking\":true,\"command\":\"" 
        part3 = executeCommand + " " + payload
        part4 = " \"}\' http://127.0.0.1/ | cut -f6 -d: | cut -f1 -d} | cut -f2 -d\\\" | base64 -d"
        cmd1 =  str(part1 + " " + part2 +  " " + part3 + " " + part4 ) 
        return cmd1

def main():
    
    parser = argparse.ArgumentParser(description="Only for Printer Configuration",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("IP", help="IP Address: e.g, 192.168.1.56")
    parser.add_argument("Port", help="Port: 5026 [pseudo environment] or 9104 [My App]")
    args = parser.parse_args()
    config = vars(args)
    print(config)
    
    HOST = sys.argv[1]
    PORT = sys.argv[2]
    TIMEOUT = 7
    print("---------------------------------------------------\n")
    print(" Please select the following cases below:\n")
    print("(0) Create interactive telnet session\n")
    print("(1) OOBE Reset the printer\n")
    print("(2) Factory Reset 4 the printer\n")
    print("(3) Check the Persona and Stack\n")
    print("(4) Change Persona to Flex and Stack to Stage\n")
    print("(5) Change Persona to Flex and Stack to Pie\n")
    print("(6) Change Persona to Flex and Stack to Prod\n")
    print("(7) Change Persona to E2E and Stack to Stage\n")
    print("(8) Change Persona to E2E and Stack to Pie\n")
    print("(9) Change Persona to E2E and Stack to Prod\n")
    print("(10) Check the unit is Permanent Dev Mode\n")
    print("(11) Set the unit to Permanent Dev Mode\n")
    print("(12) Verify the SKU unit\n")
    print("(13) Set the SKU unit\n")
    print("(14) Print the postcard\n")
    print("(15) Get the cloud id\n")
    
    print("---------------------------------------------------\n")

    i = int(input("Select one of the cases: "))
   
    print("You entered method:", i)
    if i == 0:
        print("(0) Create interactive telnet session.\n")
    if i == 1:
        print("(1) OOBE Reset the printer.\n")
    if i == 2:
        print("(2) Factory Reset 4 the printer\n")
    if i == 3:
        print("(3) Check the Persona and Stack\n")
    if i == 4:
        print("(4) Change Persona to Flex and Stack to Stage\n")
    if i == 5:
        print("(5) Change Persona to Flex and Stack to Pie\n")
    if i == 6:
        print("(6) Change Persona to Flex and Stack to Prod\n")
    if i == 7:
        print("(7) Change Persona to E2E and Stack to Stage\n")
    if i == 8:
        print("(8) Change Persona to E2E and Stack to Pie\n")
    if i == 9:
        print("(9) Change Persona to E2E and Stack to Prod\n")
    if i == 10:
        print("(10) Check the unit is Permanent Dev Mode\n")
    if i == 11:
        print("(11) Set the unit to Permanent Dev Mode\n")
    if i == 12:
        print("(12) Verify the SKU unit\n")
    if i == 13:
        print("(13) Set the SKU unit\n")
    if i == 14:
        print("(14) Print the postcard\n")
    if i == 15:
        print("(15) Get the cloud id\n")
    

    print("---------------------------------------------------\n")

    if i == 0:
        editTelnet(HOST, PORT, TIMEOUT)
    elif i == 1:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: Flex and Stack: Stage
        '''
        pseudo = [pseudoCommand.oobeReset];
        step = execute(pseudo, tn)
        
        output = toDecode(step)
        setOutput = output.split()
        nameOutput = []
        indexOutput = 0
        HotBeverageEmoji =  "\U00002615"
        for i in range(len(setOutput)):
            #print(setOutput[i])
            if '(mainApp:9104)>' == setOutput[i]:
                
                indexOutput = indexOutput + 1
                if indexOutput > 1:
                    nameOutput.append(setOutput[i])
                    #print('indexOuput passed: {}'.format(indexOutput))

            #if indexOutput:
            #    nameOutput.append(setOutput[i])
        
        #print(indexOutput)
        if indexOutput <= 1:
            print("OOBE Reset did not go through. Check your Network!")
        #print(setOutput)
        else:
            print("Done, OOBE Reset. Printer is about to reset. Have a cup of joe " + HotBeverageEmoji)
        tn.close()
        exit()

    elif i == 2:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        '''Reset 4
        '''
        pseudo = [pseudoCommand.reset4];
        step = execute(pseudo, tn)
        
        output = toDecode(step)
        setOutput = output.split()
        nameOutput = []
        indexOutput = 0
        HotBeverageEmoji =  "\U00002615"
        for i in range(len(setOutput)):
            #print(setOutput[i])
            if '(mainApp:9104)>' == setOutput[i]:
                
                indexOutput = indexOutput + 1
                if indexOutput > 1:
                    nameOutput.append(setOutput[i])
                    #print('indexOuput passed: {}'.format(indexOutput))

            #if indexOutput:
            #    nameOutput.append(setOutput[i])
        
        #print(indexOutput)
        if indexOutput <= 1:
            print("Factory Reset 4 did not go through. Check your Network!")
        #print(setOutput)
        else:
            print("Done, Factory Reset 4. Printer is about to reset. Have a cup of joe " + HotBeverageEmoji)
        tn.close()
        exit()


    elif i == 3:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Check Persona and Stack
        '''
        pseudo = [pseudoCommand.personaStatus, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        
        CRED = '\33[5m'
        CEND = '\33[0m'
        out = toDecode(step)
        #print(out)
        regex=re.compile(r"\bTRADITIONAL\b")
        if (bool(regex.findall(out)) == True):
            if (regex.findall(out)[0] == 'TRADITIONAL'):
                print(CRED + "It is set to FLEX or TRADITIONAL" + CEND)

        regex=re.compile(r"\bLOYAL\b")
        if (bool(regex.findall(out)) == True):
            if (regex.findall(out)[0] == 'LOYAL'):
                print(CRED + "It set to E2E or LOYAL" + CEND)
       
        regex=re.compile(r"\bPRODUCTION_DEVICE_TEST\b")
        if (bool(regex.findall(out)) == True):
            if regex.findall(out)[0] == 'PRODUCTION_DEVICE_TEST':
                print(CRED + "It is set to STAGE" + CEND)
        
        regex=re.compile(r"\bDEVELOPMENT\b")
        if (bool(regex.findall(out)) == True):
            if regex.findall(out)[0] == 'DEVELOPMENT':
                print(CRED + "It is set to PIE" + CEND)
        
        regex=re.compile(r"\bPRODUCTION\b")
        if (bool(regex.findall(out)) == True):
            if regex.findall(out)[0] == 'PRODUCTION':
                print(CRED + "It is set to PRODUCTION" + CEND)
        
        tn.close()
        
        # if PORT == 5026:
        #     tn5026 = telnetlib.Telnet(HOST, 5026, TIMEOUT)
        
        #     udws_command = "udws \"undercroft.ict_init;\""
        #     step = execute5026(udws_command, tn5026)
        #     print(step)
        #     #toDecode(step)
        #     tn5026.close()
            
            
        exit();
        

    elif i == 4:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: Flex and Stack: Stage
        '''
        pseudo = [pseudoCommand.setFlex, pseudoCommand.personaStatus, pseudoCommand.setStage, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        

        out = toDecode(step)
        #print(out)
        if re.search('TRADITIONAL',out):
            print("SUCCESS: Set to FLEX or TRADITIONAL")
        if re.search('PRODUCTION_DEVICE_TEST',out):
            print("SUCCESS: Set to STAGE")

        tn.close()
        
    # if PORT == 5026:
    #     tn5026 = telnetlib.Telnet(HOST, 5026, TIMEOUT)
    
    #     udws_command = "udws \"undercroft.ict_init;\""
    #     step = execute5026(udws_command, tn5026)
    #     print(step)
    #     #toDecode(step)
    #     tn5026.close()
        
        
        exit();
        
    elif i == 5:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: Flex and Stack: Pie
        '''
        pseudo = [pseudoCommand.setFlex, pseudoCommand.personaStatus, pseudoCommand.setPie, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        

        out = toDecode(step)
        #print(out)
        if re.search('TRADITIONAL',out):
            print("SUCCESS: Set to FLEX or TRADITIONAL")
        if re.search('DEVELOPMENT',out):
            print("SUCCESS: Set to PIE")

        tn.close()
        
        exit();
    
    elif i == 6:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: FLEX and Stack: Production
        '''
        pseudo = [pseudoCommand.setFlex, pseudoCommand.personaStatus, pseudoCommand.setProd, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search('TRADITIONAL',out):
            print("SUCCESS: Set to E2E or LOYAL")
        if re.search('PRODUCTION',out):
            print("SUCCESS: Set to PROD")
        
        tn.close()
        exit();

    elif i == 7:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: E2E and Stack: Stage
        '''
        pseudo = [pseudoCommand.setE2E, pseudoCommand.personaStatus, pseudoCommand.setStage, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search('LOYAL',out):
            print("SUCCESS: Set to E2E or LOYAL")
        if re.search('PRODUCTION_DEVICE_TEST',out):
            print("SUCCESS: Set to STAGE")
        
        tn.close()
        exit();

        
    elif i == 8:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: E2E and Stack: Pie
        '''
        pseudo = [pseudoCommand.setE2E, pseudoCommand.personaStatus, pseudoCommand.setPie, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search('LOYAL',out):
            print("SUCCESS: Set to E2E or LOYAL")
        if re.search('DEVELOPMENT',out):
            print("SUCCESS: Set to PIE")

        tn.close()
        exit();
    
    elif i == 9:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Setup for Persona: E2E and Stack: Production
        '''
        pseudo = [pseudoCommand.setE2E, pseudoCommand.personaStatus, pseudoCommand.setProd, pseudoCommand.stackStatus];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search('LOYAL',out):
            print("SUCCESS: Set to E2E or LOYAL")
        if re.search('PRODUCTION',out):
            print("SUCCESS: Set to PROD")
        
        tn.close()
        exit();


    elif i == 10:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Check if is Permanent UCDE Dev Mode
        '''
        pseudo = [pseudoCommand.isDevMode ];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search(' 0',out):
            print("\nIt is not Permanent UCDE Dev Mode")
        if re.search(' 1',out):
            print("\nSUCCESS: It is Permanent UCDE Dev Mode")

        tn.close()
        exit();
        
    elif i == 11:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Set to Permanent UCDE Dev Mode
        '''
        pseudo = [pseudoCommand.setDevMode ];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        
        pseudo = [pseudoCommand.isDevMode ];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search(' 0',out):
            print("\nFAILED: It is not Permanent UCDE Dev Mode")
        if re.search(' 1',out):
            print("\nSUCCESS: It is Permanent UCDE Dev Mode")
        
        tn.close()
        exit();
    elif i == 12:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        username = "root"
        password = "myroot"
    
        executeCommand = pseudoCommand.getSKUConfig
        payload = 0
        flagPayload = 0
        cmd1 = sshFormat(executeCommand, flagPayload)


        #15.1.193.255
        promptCDM = cmd1
        #print(promptCDM)
        timeout = 20
        #cmdPath = cfg_dir
        runScript = ssh_command(router_ip=HOST, router_username=username, router_password=password, cmd=promptCDM, timeout=timeout)
        output = runScript[0]
        print(f"Current SKU Number: {output}")
    
    elif i == 13:
        tn = checkConnection(HOST,PORT,TIMEOUT)
        username = "root"
        password = "myroot"
       
        executeCommand = pseudoCommand.setSKUConfig
        flagPayload = 1
        #executeCommand = payload
        cmd1 = sshFormat(executeCommand, flagPayload)
        
        #15.1.193.255
        promptCDM = cmd1
        #print(promptCDM)
        timeout = 20
        #cmdPath = cfg_dir
        runScript = ssh_command(router_ip=HOST, router_username=username, router_password=password, cmd=promptCDM, timeout=timeout)
        output = runScript[0]
        
        if re.search('0',output):
            print("Executed the command!")
        #print("Output: {output}")
    
    elif i == 14:
        # Updateing Firmware
        tn = checkConnection(HOST,PORT,TIMEOUT)
        ''' Set to Permanent UCDE Dev Mode
        '''
        pseudo = [pseudoCommand.setDevMode ];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        
        pseudo = [pseudoCommand.isDevMode ];
        step = execute(pseudo, tn)
        
        out = toDecode(step)
        #print(out)
        if re.search(' 0',out):
            print("\nFAILED: It is not Permanent UCDE Dev Mode")
        if re.search(' 1',out):
            print("\nSUCCESS: It is Permanent UCDE Dev Mode")
        
        tn.close()
        exit();

    else:
            print("\nDidn't match a case")
            exit();

main();

