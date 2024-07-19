import subprocess
import json
from config import STDOUT_DISABLE

DP = {}

# This is the main function that takes the ip as parameter
def portsResult(ip):
    try:
        if ip in DP.keys():
            return DP[ip]

        command = f'sudo masscan {ip} --top-ports 100 -oJ ./tmp/masscan_out.json --wait 0' + STDOUT_DISABLE
        subprocess.check_output(command, shell = True)

        with open('./tmp/masscan_out.json','r') as file:
            dict_list = json.loads(file.read())

        subprocess.call('rm -rf ./tmp/masscan_out.json', shell = True)

        DP[ip] = dict_list

        return dict_list
    except Exception as e:
        print(f'massscan threw the exception: {e}')
        return None

if __name__=="__main__":
    resultDictArray = portsResult("142.250.184.142")
    print(resultDictArray)