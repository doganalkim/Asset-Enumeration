import mmh3
import requests
import codecs
import shodan

def url(n):
    try:
        if "http" not in n:
    	    n = "http://" + n
        n += '/favicon.ico'
        response = requests.get(n,verify=False)
        favicon = codecs.encode(response.content, 'base64')
        hash = mmh3.hash(favicon)
        return 'http.favicon.hash:' + str(hash)
    except Exception as e:
    	print(f' Favicon hash threw exception: {e}')
    	return None

def api(favhash=None,use_api_key=False, api_key=None):
    try:
        if use_api_key:
            if api_key and favhash:
                key = shodan.Shodan(api_key)
                fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
                result = key.search(favhash, fields=fields, minify=False)
            return result
    except Exception as e:
        print(f' Favicon hash threw exception: {e}')
        return None


def sub_osint(key, domain):
    try:
        SHODAN_API_KEY = key
        subdomain = domain
        api = shodan.Shodan(SHODAN_API_KEY)

        fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
        results = api.search('hostname:' + subdomain, fields=fields, minify=False)

        return results

    except Exception as e:
        print(f' Favicon hash threw exception: {e}')
        return None

if __name__ == "__main__":
    fhash = url("https://python.org")
    fresult = api(fhash,True,"YOUR_APİ_KEY")
    sub_result = sub_osint('YOUR_APİ_KEY','DOMAİN')
    print(fresult)
    print(sub_result)
