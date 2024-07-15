from Wappalyzer import Wappalyzer, WebPage

def wappalyzer(url):
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(url)
    result = wappalyzer.analyze_with_versions_and_categories(webpage)

    for tech in result:
        result[tech] = {
            'Category': result[tech]['categories'],
            'Version': result[tech]['versions']
        }
    
    return result


# for testing purposes
if __name__=='__main__':
    result = wappalyzer('https://quotes.toscrape.com')
    print(result)