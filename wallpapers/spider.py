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


def get_page(page: int) -> str:
    return target_url + str(page+1) + '/'


async def crawl_wallpapers(loop, page: int, download_folder: str = None):
    response = await loop.run_in_executor(
        None, functools.partial(requests.get, get_page(page)))
    html = response.text
    selector = etree.HTML(html)
    imgs = selector.xpath('//div/a/img')

    def download(url: str):
        filename = f"{url[::-1].split('/', 1)[0][::-1]}"
        with open(os.path.join(download_folder, filename), 'wb') as f:
            response = requests.get(url)
            for chunk in response.iter_content(512):
                f.write(chunk)
        logger.info(f"Downloading complete {img.attrib['src']}")


    for img in imgs:
        logger.info(f"Downloading {img.attrib['src']}")
        await loop.run_in_executor(None, functools.partial(download,img.attrib['src']))



if __name__ == "__main__":
    download_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)), 'download')
    loop = asyncio.get_event_loop()
    for i in range(100):
        asyncio.ensure_future(
            crawl_wallpapers(loop, i, download_path))
    loop.run_forever()
