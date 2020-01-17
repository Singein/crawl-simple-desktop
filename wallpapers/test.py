from lxml import etree
import requests
import os

BASE_URL = "http://simpledesktops.com/"
BASE_URL_BROWSE = BASE_URL + 'browse/'

html = requests.get(BASE_URL_BROWSE).text
selector = etree.HTML(html)
imgs = selector.xpath('//div[@class="desktop"]/a')


def get_url(url: str):
    html = requests.get(url).text
    selector = etree.HTML(html)
    imgs = selector.xpath('//div[@class="desktop"]/a')
    return imgs


download_path = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'downloads')
for img in get_url(BASE_URL_BROWSE):
    url = BASE_URL + img.attrib['href'][1::]
    # print(url)
    for i in get_url(url):
        dlink = BASE_URL+i.attrib['href'][1::]
        print(dlink)
        r = requests.get(dlink)
        print(url[::-1].split('/', 2)[1][::-1])
        filename = url[::-1].split('/', 2)[1][::-1] + '.png'
        filepath = os.path.join(download_path, filename)
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(10240):
                f.write(chunk)
