import subprocess
import json
#import config

###################################################
# This script takes URL as parameter and returns  #
# the result. 'wafw00f' tool is used for this     #
# purpose. None implies no firewall               #
###################################################


def parse_file():
    with open('./tmp/waf_res.json','r') as file:
        file_content = file.read()
        if file_content:
            json_content = json.loads(file_content)
            if json_content != []:
                check_string = json_content[0]
                if check_string and 'firewall' in check_string:
                    WAF_RESULT = check_string['firewall']
                    return WAF_RESULT
    return None


# This is the main function
# Takes URL as parameter
# Result is stored as the variable 'WAF_RESULT'
# Consider the ./tmp folder issue later on
def handle_waf(url):

    # Uncomment below to test during integration
    # Output for the tool wafw00f is disabled
    #WAF_COMMAND = 'wafw00f ' + url + ' -o ./tmp/waf_res.json ' + config.STDOUT_DISABLE
    WAF_COMMAND = 'wafw00f ' + url + ' -o ./tmp/waf_res.json' + ' >/dev/null 2>&1 '

    subprocess.call(WAF_COMMAND, shell = True)

    WAF_RESULT = parse_file()

    # Delete the temporary file
    subprocess.call('rm -rf ./tmp/waf_res.json', shell = True)

    return WAF_RESULT

    # Below part can be used to eliminate false negatives of the tools
    #if not WAF_RESULT:
    #    WAF_RESULT = 'Could not be detected'

# Below is for the testing. REMOVE IT
if __name__ == '__main__':
    print(handle_waf('stackoverflow.com'))
