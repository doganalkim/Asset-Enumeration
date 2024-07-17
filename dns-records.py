import subprocess
import yaml

from config import dig_with_ip, dig_with_domain

def dig(domain: str = None, ip: str = None):
    # dns lookup
    if domain:
        cmd_output = subprocess.call(dig_dns.format(domain=domain))
    
    # reverse dns lookup
    elif ip:
        # not implemented yet
        cmd_output = subprocess.call(dig_rev_dns.format(ip=ip))

    lst = yaml.unsafe_load(cmd_output)

    return lst[0]['message']['response_message_data']

    
if __name__=='__main__':
    print(dig(domain='example.com'))
