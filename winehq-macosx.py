import urllib2
from BeautifulSoup import BeautifulSoup
import re
import json

import gecko
import mono

latest_gecko = gecko.get_latest()
latest_mono = mono.get_latest()

upstream_x86 = {
    'name': 'upstream-darwin-x86',
    'description': "Upstream darwin x86",
    'packages': []
}

upstream_amd64 = {
    'name': 'upstream-darwin-amd64',
    'description': "Upstream darwin amd64",
    'packages': []
}

staging_x86 = {
    'name': 'staging-darwin-x86',
    'description': "Staging darwin x86",
    'packages': []
}

staging_amd64 = {
    'name': 'staging-darwin-amd64',
    'description': "Staging darwin amd64",
    'packages': []
}

base_url = 'https://dl.winehq.org/wine-builds/macosx/pool/'

response = urllib2.urlopen(base_url)
html = response.read()
soup = BeautifulSoup(html)

# find table with Wine versions
prefix = "portable-winehq-"
section = soup.find('table', id='indexlist')
rows = section.findAll('tr')[1:-1]
for row in rows:
    columns = [data for data in row.findAll('td')[1:]]
    href = columns[0].a['href']
    # only portable packages and not signatures
    if href.startswith(prefix) and not href.endswith('.sig'):
        filename = href.replace(prefix, '')
        staging = filename.startswith('staging-')
        amd64 = filename.endswith('64.tar.gz')
        package = {
            'version': re.match(r'(devel|staging|stable)-(.*)-osx(64)?\.tar\.gz', filename).group(2),
            'url': base_url + href,
            'sha1sum': "",
            'geckoFile': latest_gecko['filename-x86_64'] if amd64 else latest_gecko['filename-x86'],
            'geckoUrl': latest_gecko['url-x86_64'] if amd64 else latest_gecko['url-x86'],
            'geckoMd5': None,
            'monoFile': latest_mono['filename'],
            'monoUrl': latest_mono['url'],
            'monoMd5': None
        }
        # find correct category
        if staging:
            if amd64:
                staging_amd64['packages'].append(package)
            else:
                staging_x86['packages'].append(package)
        else:
            if amd64:
                upstream_amd64['packages'].append(package)
            else:
                upstream_x86['packages'].append(package)

versions = [upstream_x86, upstream_amd64, staging_x86, staging_amd64]

with open('winehq-macosx.json', 'w') as outfile:
    json.dump(versions, outfile)
