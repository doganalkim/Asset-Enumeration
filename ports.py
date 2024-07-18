import xml.etree.ElementTree as ET
import subprocess

# This array holds the result of this script
resultDictArray = []

# These are the fields to include in the result json
serviceKeys = [
    'name',
    'product',
    'version',
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

    command = 'sudo nmap -Pn -sV -sT -oX nmap_res.xml  ' + ip + ' >/dev/null 2>&1'
    subprocess.call(command, shell = True)

    with open('nmap_res.xml','r') as file:
        stringToParse = file.read()

    subprocess.call('rm -rf nmap_res.xml', shell = True)

    root =  ET.fromstring(stringToParse)
    dfs(root)

if __name__=="__main__":
    portsResult("google.com")
    print(resultDictArray)