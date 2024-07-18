import subprocess
import json

# This is the main function that takes the ip as parameter
def portsResult(ip):

    command = f'sudo masscan {ip} --top-ports 1000 -oJ masscan_out.json --wait 0 >/dev/null 2>&1'
    subprocess.check_output(command, shell = True)

    with open('masscan_out.json','r') as file:
        dict_list = json.loads(file.read())
    

    # subprocess.call('rm -rf masscan_out.xml', shell = True)

    return dct

if __name__=="__main__":
    resultDictArray = portsResult("142.250.184.142")
    print(resultDictArray)