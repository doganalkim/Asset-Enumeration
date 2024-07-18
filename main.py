import argparse
import favicon
from config import SHODAN_API_KEY
import subprocess
import json
#import datetime

import subdomain

URL = None
IS_SHODAN_USED = False


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

# Subdomain script caller function
def find_subdomain(url):
    st = subdomain.SubdomainTools()
    st.subfinder(url)
    subdomain_result = st.get_subdomain_json()

    new_dict = {}
    new_dict['domain'] = url
    new_dict['path'] = './Subdomains/' + url + '.json'
    new_dict['subdomains'] = subdomain_result[url]

    with open('./Result/domain.json','w') as file:
        json.dump(new_dict, file, indent = 4)

    
def find_subdomain_keys():
    with open('./Result/domain.json','r') as file:
        SUBDOMAIN_LIST = json.loads(file.read())['subdomains']


def main():

    parse_args()

    if not URL:
        return None

    try:
        # Remove the result and temporary folders and create them back
        #subprocess.call('rm -rf tmp && mkdir tmp && rm -rf Result && mkdir Result \
        #                && mkdir ./Result/Subdomains', shell = True)


        #find_subdomain(URL)

        find_subdomain_keys()

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