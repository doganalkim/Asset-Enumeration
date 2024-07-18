import mmh3
import requests
import codecs
import shodan

def url(n):
    n += '/favicon.ico'
    response = requests.get(n,verify=False)
    favicon = codecs.encode(response.content, 'base64')
    hash = mmh3.hash(favicon)
    print('\nShodan search query: http.favicon.hash:' + str(hash))
    return str(hash)

def api(favhash=None,use_api_key=False, api_key=None):
    if use_api_key:
        if api_key and favhash:
            key = shodan.Shodan(api_key)
            fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
            result = key.search('http.favicon.hash:' + favhash, fields=fields, minify=False)
            count = 1
            for service in result['matches']:
                for field in fields:
                    print(field + ": " + str(service.get(field, 'Not Available')))
                print("\n\n")

def main():
    test = url('https://www.python.org/favicon.ico')

    api_key = '' #Please enter your own Shodan API key.
    api = shodan.Shodan(api_key)
    print("\n")
    fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
    result = api.search('http.favicon.hash:' + test,fields=fields ,minify=False)
    count=1
    for service in result['matches']:
        for field in fields:
            print(field + ": " + str(service.get(field, 'Not Available')))
        print("\n\n")


if __name__ == "__main__":
    #main()
    x=url("https://python.org")
    api(x,True,"cZDG3xexLwRShMxzDLYHENtiOxUAqFV1")