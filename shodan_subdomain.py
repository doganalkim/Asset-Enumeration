import shodan

def sub_osint(key, domain):
    SHODAN_API_KEY = key
    subdomain = domain
    api = shodan.Shodan(SHODAN_API_KEY)


    fields = ["ip_str", "port", "hostnames", "org", "isp", "asn", "os", "location", "domains", "product", "version", "cpe"]
    results = api.search('hostname:' + subdomain)

    for service in results['matches']:
        for field in fields:
            print(field + ": " + str(service.get(field, 'Not Available')))
        print("\n\n")
if __name__ == "__main__":
    sub_osint('YOUR_APİ_KEY','SUBDOMAİN')