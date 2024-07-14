import re
import subprocess
import json

####################################################################
# Explanation of this file                                         #
# This code segment returns the result of the whois as json format #
####################################################################

whoisDictResult = {}   # Initializing as an empty dictionary


# These arrays are some of the exceptions to exclude from resulting match.
# These arrays can be manipulated for exclusion in the future.
# For example, if we can use command line argument to exclude,
# then it is enough to add related parameter to this array in
# order to exclude from the resulting json
KeyExceptions = [ \
    'NOTICE', \
    'TERMS OF USE', \
    'by the following terms of use', \
]

ValueExceptions = [\
    '(1) allow, enable, or otherwise support the transmission of mass'
]

def parse(stringToParse):
    global KeyExceptions, ValueExceptions
    searchResult = re.findall("\s*>*\s*(.*): (.*)", stringToParse)
    for i in range(len(searchResult)):
        key = searchResult[i][0]
        value = searchResult[i][1]
        if key not in KeyExceptions and \
                value not in ValueExceptions:                               # If not in exceptions
            whoisDictResult.update({key:value})                             # Add to dictionary for each element

    #return json.dumps(DictResult, indent=4)                                # result is json

# USE THIS FUNCTION TO GET THE RESULT
# Required parameter is the URL of the target
def whoisResult(url):
    # Execute whois
    command = 'whois ' + url
    whoisOutput = subprocess.check_output(command, shell=True).decode()
    parse(whoisOutput)

# Below functions can be used to expand exceptions
def addKeyException(key):
    KeyExceptions.append(key)

def addValueException(value):
    ValueExceptions.append(value)
