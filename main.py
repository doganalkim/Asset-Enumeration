# LIBRARIES
import argparse
from config import SHODAN_API_KEY
import subprocess
import json
#import datetime

# SCRIPTS
import subdomain
import dns_records
import waf
import masscan
import whois
import wappalyzer
import shodan_tools

URL = None
IS_SHODAN_USED = False
SUBDOMAIN_ARRAY_RESULT = []


def parse_args():
    global URL

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        dest='n',
                        metavar='',
                        help='Enter the target URL address')

    parser.add_argument('-s', '--shodan',
                        action='store_true',
                        help='Enter this parameter to use your Shodan API key')

    args = parser.parse_args()

    URL = args.n

    if URL:
        IS_SHODAN_USED = args.shodan

# Subdomain script caller function ( level 1 json creator )
def find_subdomain(url):
    st = subdomain.SubdomainTools()
    st.subfinder(url)
    subdomain_result = st.get_subdomain_json()

    new_dict = {}
    new_dict['domain'] = url
    new_dict['path'] = './Subdomains/' + url + '.json'
    new_dict['whois'] = whois.whoisResult(url)
    new_dict['subdomains'] = subdomain_result[url]

    with open('./Result/domain.json','w') as file:
        json.dump(new_dict, file, indent = 4)

# Level 2 json creator
def subdomain_filler(sd, domain):
    # Create the dictionary
    print(sd)
    dict_res = {} #create_dict()
    dict_res['main-domain'] = domain
    dict_res['subdomain name'] = sd

    # UNCOMMENT THEM TO TEST IT
    dns_records_result = dns_records.dig(sd)

    dict_res['Primary IP'] = None

    # If the result is non empty array.
    # This means if everything goes well
    if dns_records_result != []:
        dict_res['DNS'] = dns_records_result[0]

        dict_res['IPs'] = dns_records_result[1]

        dict_res['Primary IP'] = dns_records_result[2]

    dict_res['WAF'] = waf.handle_waf(sd)

    if dict_res['Primary IP']:
        dict_res['Web Technologies'] = wappalyzer.wappalyzer(sd)

    if dict_res['Primary IP']: 
        dict_res['ports'] = masscan.portsResult(dict_res['Primary IP'])


    #print(dict_res)

    return dict_res

# Level 3 json creator
def endpoint_filler(sd):
    return None

def subdomain_json_filler():
    with open('./Result/domain.json','r') as file:
        SUBDOMAIN_LIST = json.loads(file.read())['subdomains']
    
    for subdomain in SUBDOMAIN_LIST:
        try:
            SUBDOMAIN_ARRAY_RESULT.append(subdomain_filler(subdomain,URL))
        except Exception as e:
            print(f'{e}')
            continue

    with open('./Result/Subdomains/subdomains.json','w') as file:
    	json.dump(SUBDOMAIN_ARRAY_RESULT, file, indent = 4)


def main():

    parse_args()

    if not URL:
        raise Exception('Provide a URL')

    try:
        # Remove the result and temporary folders and create them back
        subprocess.call('rm -rf tmp && mkdir tmp && rm -rf Result && mkdir Result \
                        && mkdir ./Result/Subdomains', shell = True)

        # This is for level 1 json file
        find_subdomain(URL)

        # This is for level 2 json file
        subdomain_json_filler()

        """
        if args.n:
            test = favicon.url(n=args.n)

            if args.shodan:
                favicon.api(favhash=str(test), use_api_key=True, api_key=args.api_key)
            else:
                favicon.api(use_api_key=False)
        """
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
