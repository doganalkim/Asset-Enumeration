from Wappalyzer import Wappalyzer, WebPage


def wappalyzer(domain):
    """Do a web tech scan to provided domain.

    :param str domain: domain name with no schemes
    """
    
    schemes = [
        'http://',
        'https://' # cert error can occur
    ]

    result = dict()
    title = None

    wappalyzer = Wappalyzer.latest()

    for scheme in schemes:
        try:
            webpage = WebPage.new_from_url(scheme + domain, timeout=4)
        except Exception as e:
            print(f'Wappalyzer threw exception: {e}')
            continue
        
        # get the title
        if not title:
            title = webpage.parsed_html.title.text

        wapp_out = wappalyzer.analyze_with_versions_and_categories(webpage)

        for tech in wapp_out:
            result[scheme.removesuffix('://')] = {
                'Tech': tech,
                'Category': wapp_out[tech]['categories'],
                'Version': wapp_out[tech]['versions']
            }
    
    return [result, title]


# for testing purposes
if __name__=='__main__':
    result, t = wappalyzer('quotes.toscrape.com')
    print(result, t)