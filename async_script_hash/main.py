import asyncio
import aiohttp
import hashlib
import zipfile
import os
import time


basedir = os.path.abspath(os.path.dirname(__file__))
directory = basedir + '/project-configuration'

# саздание временной директории
if not os.path.exists(basedir + "/dir-zip"):
    time_dir = os.mkdir(basedir + "/dir-zip")


async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            with open(basedir + '/dir-zip/repository.zip', 'wb') as file:
                file.write(content)
            return content


def unzip_the_archive():
    '''Распаковка архива и его последующее удаление'''

    zippath = zipfile.ZipFile(basedir + '/dir-zip/repository.zip')
    zippath.extractall(basedir + '/')

    # удаление архива и временной директории
    os.remove(basedir + '/dir-zip/repository.zip')
    os.rmdir(basedir + '/dir-zip')

    zippath.close()


def get_hash():
    """Вычисление хеша файлов"""

    hash_list = []
    
    for root, _, files in os.walk(directory):
        for i in files:
            hash_list.append(root + '/' + i)

    res = []
    for i in hash_list:
        with open(i, 'rb') as f:
            sha256_hash = hashlib.sha256()
            while True:
                data = f.read(2048)
                if not data:
                    break
                sha256_hash.update(data)
            rez = sha256_hash.hexdigest()
            res.append(rez)
    
    return res


async def main():
    t1 = time.time()
    url = 'https://gitea.radium.group/radium/project-configuration/archive/master.zip'
    tasks = []
    for _ in range(3):
        task = asyncio.create_task(download_file(url))
        tasks.append(task)

    await asyncio.gather(*tasks)
    unzip_the_archive()
    # print(get_hash())
    t2 = time.time()
    print(t2 - t1)
    return get_hash()


if __name__ == '__main__':
    asyncio.run(main())