import os

import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

class ImageData:
    
    def __init__(self, name, img_url):
        self.name = name
        self.img_url = img_url



async def main():
    url ='https://commons.wikimedia.org/wiki/Category:Pictures_of_the_day_(2022)'

    async with aiohttp.ClientSession() as session:
        content = await session.get(url)
        # print(await content.text())

       # Parsing web page with BeautifulSoup
        soup = BeautifulSoup(await content.text(), 'html.parser')
        images = []

        image_blocks = soup.find_all('li', {'class': 'gallerybox'})
        # print(image_blocks)

        count = 0
        for block in image_blocks:
            count += 1
            if count > max_images:
                break
        # block = image_blocks[0]
            
            imgs = block.find_all('img')
            if len(imgs) > 0:
                    img_url = imgs[0]['src']

                    header = block.find('div', {'class': 'gallerytext'})
                    link = header.find('a')
                    title = link.text
                    # print(count)

                    images.append(ImageData(title, img_url))

            # create images folder if it doesn't exist
            if not os.path.exists('images'):
                os.makedirs('images')
            
        count = 0
        lst = []
        for image in images:
            count += 1
            lst.append(download_and_save(image.img_url, f'images/{count}.jpg', session))
        
        await asyncio.gather(*lst)
            

async def download_and_save(url, name, session):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.read()

            f = open(name, "wb")
            f.write(data)
            f.close()




if __name__ == '__main__':
    print("z")
    max_images = 300
    asyncio.run(main())