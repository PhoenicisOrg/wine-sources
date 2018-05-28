import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import re


def get_url():
    base_url = 'https://dl.winehq.org/wine/wine-gecko/'

    response = urllib2.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html)

    # find table with gecko versions
    versions = []
    section = soup.find('table', id='indexlist')
    rows = section.findAll('tr')[1:]
    for row in rows:
        columns = [data for data in row.findAll('td')[1:]]
        href = columns[0].a['href']
        # only rows with versions which are not e.g. beta
        if re.match(r'^\d+\.\d+(\.\d+)?/$', href):
            date_string = columns[1].contents[0]
            date_string = date_string.strip()
            version = {
                'version': href,
                'url': base_url + href,
                'date': datetime.strptime(date_string, '%Y-%m-%d %H:%M'),
            }
            versions.append(version)

    # get newest version
    versions.sort(key=lambda v: v['date'], reverse=True)

    return versions[0]['url']