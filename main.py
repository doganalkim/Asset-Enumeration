# LIBRARIES
import argparse

import ports
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
from endpoint import EndpointScanTools
import shodan_tools
import config
import ipfinder

URL = None
IS_SHODAN_USED = False
SUBDOMAINS = []
FAV_HASH = None

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


def shodan_api_caller(fav_hash):
    if fav_hash and config.SHODAN_API_KEY != '':
        return shodan_tools.api(fav_hash, True, config.SHODAN_API_KEY )
    else:
        return None


# Subdomain script caller function ( level 1 json creator )
def find_subdomain(url):
    global SUBDOMAINS, FAV_HASH

    st = subdomain.SubdomainTools()
    st.subfinder(url)
    subdomain_result = st.get_subdomain_json()

    new_dict = {}
    new_dict['domain'] = url
    new_dict["favicon hash"] = shodan_tools.url(url)
    FAV_HASH = new_dict["favicon hash"] 
    new_dict['Favicon Query'] =  shodan_api_caller(FAV_HASH)
    new_dict['IP'] = ipfinder.get_ip(url)
    new_dict['Shodan'] = shodan_tools.sub_osint(config.SHODAN_API_KEY , url, new_dict['IP'])
    #new_dict['path'] = './Subdomains/' + url + '.json'
    new_dict['whois'] = whois.whoisResult(url)
    new_dict['subdomains'] = subdomain_result[url]
    SUBDOMAINS = subdomain_result[url]

    with open('./Result/domain.json','w') as file:
        json.dump(new_dict, file, indent = 4)
    #print(new_dict)
    
def shodan_subdomain_filler(url, ip):
    if config.SHODAN_API_KEY !="":
        dict_result = shodan_tools.sub_osint( config.SHODAN_API_KEY , url, ip)
        if 'total' in dict_result.keys() and dict_result['total'] > 0:
            return dict_result
    return None


# Level 2 json creator
def subdomain_filler(sd, domain):
    # Create the dictionary
    print(sd)

    
    dict_res = {} #create_dict()
    dict_res['main-domain'] = domain
    dict_res['subdomain name'] = sd

    # UNCOMMENT THEM TO TEST IT
    dns_records_result = dns_records.dig(sd)

    dict_res['Primary IP'] = ipfinder.get_ip(sd)

    # If the result is non empty array.
    # This means if everything goes well
    if dns_records_result != []:
        dict_res['DNS'] = dns_records_result[0]

        dict_res['IPs'] = dns_records_result[1]

    dict_res['WAF'] = waf.handle_waf(sd)


    if dict_res['Primary IP']:
        dict_res['Shodan'] = shodan_subdomain_filler(sd, dict_res['Primary IP'])

        dict_res['Web Technologies'], dict_res['Title'] = wappalyzer.wappalyzer(sd)

        #dict_res['ports'] = masscan.portsResult(dict_res['Primary IP'])
        dict_res['ports'] = ports.portsResult(dict_res['Primary IP'])


    #print(dict_res)

    return dict_res

# Level 3 json creator
def endpoint_json_filler():
    global SUBDOMAINS
    endpoints = []

    subdomain_list = SUBDOMAINS
    
    est = EndpointScanTools()

    for subdomain in subdomain_list:
        try:
            est.scrapy(allowed_domains=subdomain_list, start_urls=[f'http://{subdomain}'])

        except Exception as e:
            print(f'{e}')
            continue

        with open('tmp/endpoints.txt') as f:
            endpoints = f.read().split('\n')

        with open(f'./Result/Subdomains/{subdomain}.json','w') as file:
            json.dump({subdomain: endpoints}, file, indent = 4)

def subdomain_json_filler():
    global SUBDOMAINS
    subdomain_array_result = []

    subdomain_list = SUBDOMAINS
    
    for subdomain in subdomain_list:
        try:
            #subdomain_array_result.append(subdomain_filler(subdomain,URL))
            subdomain_dict = subdomain_filler(subdomain,URL)
            with open('./Result/Subdomains/'+ subdomain + '.json', 'w') as f:
                json.dump(subdomain_dict, f, indent = 4)
        except Exception as e:
            print(f'{e}')
            continue

    #with open('./Result/Subdomains/subdomains.json','w') as file:
    #	json.dump(subdomain_array_result, file, indent = 4)


def main():
    parse_args()

    if not URL:
        raise Exception('Provide a URL')

    try:
        # Remove the result and temporary folders and create them back
        subprocess.call('rm -rf tmp && mkdir tmp && rm -rf Result && mkdir Result \
                        && mkdir ./Result/Subdomains ', shell = True)

        # This is for level 1 json file
        find_subdomain(URL)

        # This is for level 2 json file
        subdomain_json_filler()

        # Level 3 json file. endpoints for each subdomain
        #endpoint_json_filler()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
