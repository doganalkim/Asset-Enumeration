import argparse
import favicon

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url',
                        dest='n',
                        metavar='',
                        help='Enter the target URL address')
    parser.add_argument('-k', '--key',
                        dest='api_key',
                        metavar='',
                        help='Enter this parameter to use your Shodan API key')

    args = parser.parse_args()

    if args.n:
        test = favicon.url(n=args.n)

        if args.api_key:
            favicon.api(favhash=str(test), use_api_key=True, api_key=args.api_key)
        else:
            favicon.api(use_api_key=False)

if __name__ == "__main__":
    main()