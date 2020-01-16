import requests
from lxml import etree
import asyncio
import functools
import future

target_url = "http://simpledesktops.com/browse/"

# html = requests.get(target_url).text
# selector = etree.HTML(html)
# imgs = selector.xpath('//div/a/img')
# for img in imgs:
#     print(img.attrib['src'])


def crawl_wallpapers(pages: int, processer: int, download_folder: str):
    pass


async def get_html(url: str):
    print('start get')
    future = asyncio.get_event_loop().run_in_executor(
        None, functools.partial(requests.get, url))
    response = await future
    print(response.text)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(get_html('http://simpledesktops.com/browse/')))
