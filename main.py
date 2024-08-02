# LIBRARIES
import argparse

from config import SHODAN_API_KEY
import subprocess
import json
import datetime

# SCRIPTS
import subdomain
import dns_records
import waf
#import masscan # It uses masscan for port scanning
import ports   # It uses Nmap for port scanning
import whois
import wappalyzer
import shodan_tools
import config
import ipfinder

URL = None
SUBDOMAINS = []
FAV_HASH = None



# Function for parsing command line url
def parse_args():
    global URL

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        dest='n',
                        metavar='',
                        help='Enter the target URL address')

    #  This may be used in the future for Shodan part
    #parser.add_argument('-s', '--shodan',
    #                    action='store_true',
    #                    help='Enter this parameter to use your Shodan API key')

    args = parser.parse_args()

    URL = args.n


def shodan_api_caller(fav_hash):
    if fav_hash and config.SHODAN_API_KEY != '':
        return shodan_tools.api(fav_hash, True, config.SHODAN_API_KEY )
    else:
        return None


# Subdomain script caller function ( level 1 json creator )
def find_subdomain(url):
    global SUBDOMAINS, FAV_HASH
    dns_result = dns_records.dig(URL)
    # First find each subdomain
    st = subdomain.SubdomainTools()
    st.subfinder(url)
    subdomain_result = st.get_subdomain_json()

    key = "Shodan"

    # Create the dictionary data structure
    new_dict = {}
    new_dict['domain'] = url
    new_dict['Timestamp'] = config.CUR_TIME
    new_dict['IPs'] = dns_result[1]
    new_dict["Favicon hash"] = shodan_tools.get_favicon_url(url)
    FAV_HASH = new_dict["Favicon hash"] 
    new_dict['Favicon Query'] =  shodan_api_caller(FAV_HASH)
    new_dict['WAF'] = waf.handle_waf(url)
    for ip in new_dict['IPs']:
        if key not in new_dict:
            new_dict[key] = []
        new_dict[key].append(shodan_tools.sub_osint(config.SHODAN_API_KEY , url, ip))    
    new_dict['whois'] = whois.whoisResult(url)
    new_dict['subdomains'] = subdomain_result[url]
    SUBDOMAINS = subdomain_result[url]

    # Write the result into JSON
    with open('./Result/domain.json','w') as file:
        json.dump(new_dict, file, indent = 4)
    
def shodan_subdomain_filler(url):
    if config.SHODAN_API_KEY !="":
        dict_result = shodan_tools.sub_osint( config.SHODAN_API_KEY , url)
        if 'total' in dict_result.keys() and dict_result['total'] > 0:
            return dict_result
    return None


# Level 2 json creator
def subdomain_filler(sd, domain):
    # Create the dictionary
    #print(sd)
    key ="ports"
    dict_res = {} #create_dict()
    dict_res['main-domain'] = domain
    dict_res['subdomain name'] = sd
    dict_res['Timestamp'] = config.CUR_TIME

    # UNCOMMENT THEM TO TEST IT
    dns_records_result = dns_records.dig(sd)

    #dict_res['Primary IP'] = ipfinder.get_ip(sd)

    # If the result is non empty array.
    # This means if everything goes well
    if dns_records_result != []:
        dict_res['IPs'] = dns_records_result[1]
        dict_res['DNS'] = dns_records_result[0]

    dict_res['WAF'] = waf.handle_waf(sd)

    # Fill the keys below if the target subdomain has IP ( active server)
    if dict_res['IPs']:
        dict_res['Favicon hash'] = shodan_tools.get_favicon_url(sd)
        FAVİCON_HASH = dict_res["Favicon hash"] 
        dict_res['Favicon Query'] =  shodan_api_caller(FAVİCON_HASH)
        dict_res['Shodan'] = shodan_subdomain_filler(sd)
        dict_res['Web Technologies'], dict_res['Title'] = wappalyzer.wappalyzer(sd)

        #dict_res['ports'] = masscan.portsResult(dict_res['Primary IP'])
        for ip in dict_res['IPs']:
            if key not in dict_res:
                dict_res[key] = []
            dict_res[key].append(ports.portsResult(ip))
        #dict_res['ports'] = ports.portsResult(dict_res['Primary IP'])

    return dict_res

# Iterates through each subdomain and writes the resulting JSON
def subdomain_json_filler():
    global SUBDOMAINS

    subdomain_list = SUBDOMAINS
    
    for subdomain in subdomain_list:
        try:
            #subdomain_array_result.append(subdomain_filler(subdomain,URL))
            subdomain_dict = subdomain_filler(subdomain,URL)

            # Result will be stored in ($subdomain_name).json file under ./Result/Subdomains/ directory.
            with open('./Result/Subdomains/'+ subdomain + '.json', 'w') as f:
                json.dump(subdomain_dict, f, indent = 4)
        except Exception as e:
            print(f'{e}')
            continue


# Get the current time for Timestamp
def get_time():
    config.CUR_TIME = str(datetime.datetime.now())

# Save the endpoints in tmp directory to Result directory in JSON format.
# Also adds a timestamp.
def _save_endpoints(filename: str):
    filename = filename.replace(' ', '').replace(',', '_').replace('.', '-')
    
    with open('./tmp/endpoints.txt') as f:
        endpoints = f.read().split('\n')

    dct = {
        "Timestamp": config.CUR_TIME,
        "Endpoints": endpoints
    }

    subprocess.call('mkdir -p ./Result/Endpoints ', shell = True)

    with open('./Result/Endpoints/'+ filename + '.json', 'w') as f:
        json.dump(dct, f, indent = 4)

def main(url=None):
    global URL
    if url:
        URL = url
    else:
        parse_args()

    get_time()

    # URL not provided by user
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


    except Exception as e:
        print(e)
        return "failed"

    return "success"

if __name__ == "__main__":
    main()
    
