import subprocess
import yaml
import json

from config import dig_dns, dig_rev_dns

def dig(domain: str = None, ip: str = None):
    if not domain and not ip:
        raise Exception('Error: provide domain or IP')
    
    # dns lookup
    if domain:
        cmd_output = subprocess.check_output(dig_dns.format(domain=domain), shell=True)
    
    # reverse dns lookup
    elif ip:
        # not implemented yet
        cmd_output = subprocess.check_output(dig_rev_dns.format(ip=ip), shell=True)

    lst = yaml.unsafe_load(cmd_output)

    dns_response = lst[0]['message']['response_message_data']
    try:
        answer = dns_response['ANSWER_SECTION']
    except Exception as e:
        # domain not available, no answer
        raise e
        
    if domain:
        _extract_ip(answer, domain)
    
    return [dns_response, ips, ips[0]]

def _extract_ip(ans: list, domain):
    ips = []
    
    for i in ans:
        ips.append(i.split('IN A ')[-1])

    # the ip ping command chooses to send packets inserted to the head of list 
    if domain:
        the_best_ip = subprocess.check_output(f'ping -c 2 {domain}', shell=True)
        ips.remove(the_best_ip)
        ips.insert(0, the_best_ip)


if __name__=='__main__':
    a = (dig('acunn.com'))
