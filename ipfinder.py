import socket
import subprocess

def get_ip(domain):
    try:
        # Get the IP address from the domain name
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None
  
  
if __name__ == '__main__':
    print(get_ip('toscrape.com'))
