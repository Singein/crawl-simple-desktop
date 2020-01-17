import requests
from lxml import etree
import asyncio
import os
import functools
from concurrent.futures import Future
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(module)s %(message)s')
logger = logging.getLogger('Papers')


target_url = "http://simpledesktops.com/browse/"
BASE_URL = "http://simpledesktops.com/"


def get_page(page: int) -> str:
    return target_url + str(page+1) + '/'


def get_url(url: str):
    html = requests.get(url).text
    selector = etree.HTML(html)
    imgs = selector.xpath('//div[@class="desktop"]/a')
    return imgs


async def crawl_wallpapers(loop, page: int, download_folder: str = None):
    imgs = await loop.run_in_executor(
        None, functools.partial(get_url, get_page(page)))
    # html = response.text
    # selector = etree.HTML(html)
    # imgs = selector.xpath('//div[@class="desktop"]/a')

    def download(url: str, filename):
        # filename = f"{url[::-1].split('/', 1)[0][::-1]}"
        with open(os.path.join(download_folder, filename), 'wb') as f:
            response = requests.get(url)
            for chunk in response.iter_content(512):
                f.write(chunk)
        logger.info(f"Downloading complete {img.attrib['href']}")

    def get_img_download_link(img):
        imgs = get_url(BASE_URL + img.attrib['href'][1::])
        for i in imgs:
            return BASE_URL+i.attrib['href'][1::]

    for img in imgs:
        logger.info(f"Downloading {img.attrib['href']}")
        filename = img.attrib['href'][::-1].split('/', 2)[1][::-1] + '.png'
        download_link = await loop.run_in_executor(None, functools.partial(get_img_download_link, img))
        await loop.run_in_executor(None, functools.partial(download, download_link, filename))

if __name__ == "__main__":
    download_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'download')
    loop = asyncio.get_event_loop()
    for i in range(10, 200):
        asyncio.ensure_future(
            crawl_wallpapers(loop, i, download_path))
    loop.run_forever()
