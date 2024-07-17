import subprocess
import json
#import config

###################################################
# This script takes URL as parameter and returns  #
# the result. 'wafw00f' tool is used for this     #
# purpose. None implies no firewall               #
###################################################

WAF_RESULT = None

def parse_file():
    global WAF_RESULT
    with open('./tmp/waf_res.json','r') as file:
        WAF_RESULT = json.loads(file.read())[0]['firewall']

# This is the main function
# Takes URL as parameter
# Result is stored as the variable 'WAF_RESULT'
# Consider the ./tmp folder issue later on
def handle_waf(url):
    global WAF_RESULT

    # Uncomment below to test during integration
    # Output for the tool wafw00f is disabled
    #WAF_COMMAND = 'wafw00f ' + url + ' -o ./tmp/waf_res.json ' + config.STDOUT_DISABLE
    WAF_COMMAND = 'wafw00f ' + url+ ' -o ./tmp/waf_res.json' + ' >/dev/null 2>&1 '

    subprocess.call(WAF_COMMAND, shell = True)

    parse_file()

    # Delete the temporary file
    subprocess.call('rm -rf ./tmp/waf_res.json', shell = True)

    # Below part can be used to eliminate false negatives of the tools
    #if not WAF_RESULT:
    #    WAF_RESULT = 'Could not be detected'

# Below is for the testing. REMOVE IT
if __name__ == '__main__':
    handle_waf('stackoverflow.com')
    print(WAF_RESULT)
