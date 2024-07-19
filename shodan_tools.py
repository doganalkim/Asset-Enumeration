import mmh3
import requests
import codecs
import shodan

def url(n):
    n += '/favicon.ico'
    response = requests.get(n,verify=False)
    favicon = codecs.encode(response.content, 'base64')
    hash = mmh3.hash(favicon)
    return str(hash)

def api(favhash=None,use_api_key=False, api_key=None):
    if use_api_key:
        if api_key and favhash:
            key = shodan.Shodan(api_key)
            fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
            result = key.search('http.favicon.hash:' + favhash, fields=fields, minify=False)
    return result


def sub_osint(key, domain):
    SHODAN_API_KEY = key
    subdomain = domain
    api = shodan.Shodan(SHODAN_API_KEY)


    fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
    results = api.search('hostname:' + subdomain, fields=fields, minify=False)

    return results

if __name__ == "__main__":
    fhash = url("https://python.org")
    fresult = api(fhash,True,"YOUR_APİ_KEY")
    sub_result = sub_osint('YOUR_APİ_KEY','DOMAİN')
    print(fresult)
    print(sub_result)