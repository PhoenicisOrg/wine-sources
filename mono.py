import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_latest():
    base_url = 'https://dl.winehq.org/wine/wine-mono'

    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, features="html5lib")

    # find table with gecko versions
    versions = []
    section = soup.find('table', id='indexlist')
    rows = section.findAll('tr')[1:]
    for row in rows:
        columns = [data for data in row.findAll('td')[1:]]
        href = columns[0].a['href']
        # only rows with versions which are not e.g. beta
        if re.match(r'^\d+\.\d+(\.\d+)?/$', href):
            version_name = href[:-1]
            file_name = "wine-mono-{0}.msi".format(version_name)
            date_string = columns[1].contents[0]
            date_string = date_string.strip()
            version = {
                'version': version_name,
                'filename': file_name,
                'url': "{0}/{1}/{2}".format(base_url, version_name, file_name),
                'date': datetime.strptime(date_string, '%Y-%m-%d %H:%M'),
            }
            versions.append(version)

    # get newest version
    versions.sort(key=lambda v: v['date'], reverse=True)

    return versions[0]
