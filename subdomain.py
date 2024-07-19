import subprocess
import json
from config import subfinder_command


class SubdomainTools:
    dct = {}

    def subfinder(self, domain: str):
        # Execute subfinder
        command = subfinder_command.format(DOMAIN=domain)
        subdomains = subprocess.check_output(command, shell=True).decode()

        # reshape the output
        subdomains = subdomains.split('\n')[:-1]

        self._add_to_dict(domain, subdomains)

    def _add_to_dict(self, domain, subdomains):
        if domain not in self.dct.keys():
            # create key value pair
            self.dct[domain] = subdomains
        else:
            # append subdomains to existing subdomains
            self.dct[domain] = list(set(self.dct[domain] + subdomains))

    def get_subdomain_json(self):
        # Use one of below ( either dictionary or json)
        return self.dct
        #return json.dumps(self.dct)


# for testing purposes
if __name__=='__main__':
    st = SubdomainTools()
    st.subfinder('yandex.com')
    print(st.get_subdomain_json())