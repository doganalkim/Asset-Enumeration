from Wappalyzer import Wappalyzer, WebPage


def wappalyzer(domain):
    """Do a web tech scan to provided domain.

    :param str domain: omain name with no schemes
    """
    
    schemes = [
        'http://',
        'https://' # cert error can occur
    ]

    result = dict()

    wappalyzer = Wappalyzer.latest()

    for scheme in schemes:
        try:
            webpage = WebPage.new_from_url(scheme + domain)
        except Exception as e:
            print(f'Wapalyzer threw exception: {e}')
            continue
            
        wapp_out = wappalyzer.analyze_with_versions_and_categories(webpage)

        for tech in wapp_out:
            result[scheme.removesuffix('://')] = {
                'Tech': tech,
                'Category': wapp_out[tech]['categories'],
                'Version': wapp_out[tech]['versions']
            }
    
    return result


# for testing purposes
if __name__=='__main__':
    result = wappalyzer('antivirus1.vulnweb.com')
    print(result)