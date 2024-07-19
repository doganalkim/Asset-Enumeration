import xml.etree.ElementTree as ET
import subprocess

# This array holds the result of this script
resultDictArray = []

# These are the fields to include in the result json
serviceKeys = [
    'name',
    'product',
    'version',
    'service'
    ]

# Function for parsing service
def handle_service(service, dictResult):
    attribs = service.attrib

    for key,value in attribs.items():
        if key in serviceKeys:
            dictResult[key] = value

    return dictResult

# Function for parsing ports
def handle_port(port):
    dictResult = {}
    attribs = port.attrib

    for key,value in attribs.items():
        dictResult[key] = value

    for child in port:
        if child.tag == 'service':
            dictResult = handle_service(child,dictResult)

    resultDictArray.append(dictResult)

# XML is stored as tree, I use depth first search in
# order to traverse the tree and find the required fields
def dfs(node):
    if node.tag == 'port':
        handle_port(node)
    else:
        for child in node:
            dfs(child)

# This is the main function that takes the ip as parameter
def portsResult(ip):

    global resultDictArray
    resultDictArray = []

    command = 'sudo nmap -Pn -sT -sV -p 80,443 -oX ./tmp/nmap_res.xml  ' + ip #+ ' >/dev/null 2>&1 '
    subprocess.call(command, shell = True)

    with open('./tmp/nmap_res.xml','r') as file:
        stringToParse = file.read()

    subprocess.call('rm -rf ./tmp/nmap_res.xml', shell = True)

    root =  ET.fromstring(stringToParse)
    dfs(root)

    return resultDictArray

if __name__=="__main__":
    print(portsResult("geeksforgeeks.com"))