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

    if 'response_message_data' not in cmd_output.decode():
        return []

    lst = yaml.unsafe_load(cmd_output)

    dns_response = lst[0]['message']['response_message_data']
    try:
        answer = dns_response['ANSWER_SECTION']
    except Exception as e:
        # domain not available, no answer
        raise e
        
    if domain:
        return [dns_response] + list(_extract_ip(answer, domain))

    return [dns_response, [], '']

def _extract_ip(ans: list, domain):
    ips = []
    the_best_ip = ''

    for i in ans:
        ips.append(i.split('IN A ')[-1])

    if len(ips) == 0:
        return ips, the_best_ip

    try:
        # the ip ping command chooses to send packets inserted to the head of list
        if domain:
            cmd_out = subprocess.check_output(f'ping -c 2 {domain}', shell=True).decode()
            the_best_ip = cmd_out[cmd_out.find('(') + 1:cmd_out.find(')')]
            ips.remove(the_best_ip)
            ips.insert(0, the_best_ip)

        return ips, the_best_ip
    except Exception as e:
        print(f'DNS records threw the exception: {e}')
        return []

if __name__=='__main__':
    print(dig('examplenoktacom'))
