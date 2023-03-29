"""
Тестовой задание.

Скрипт выполненого тестового задания по асинхронному скачиванию
файлов из удаленного репозитария и вычисления их хеша.
"""
import asyncio
import hashlib
import os

import aiofiles
import aiohttp

url = 'https://gitea.radium.group/radium/project-configuration/raw/branch/master/'

url_list_file = 'https://gitea.radium.group/radium/project-configuration/tree-list/branch/master'

SIZE = 2048
NUMBER_OF_TREADS = 12
BASEDIR = os.path.abspath(os.path.dirname(__file__))
temporary_directory_path = '{basedir}/project-configuration/'.format(
    basedir=BASEDIR,
)

# саздание временной директории
if not os.path.exists(temporary_directory_path):
    os.mkdir(temporary_directory_path)


async def download_list_name_file(link):
    """Получение списка файлов репозитария.

    Args:
        link: ссылка на страницу списка с именами файлов
            хранящимися в репозитарии

    Returns:
        list_name (list): список имен файлов репозитария
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(link, allow_redirects=True) as response:
            return await response.json()


async def download_file(link, name, sem):
    """Скачивание файлов из репозитария.

    Args:
        link: ссылка для построения полного  url файла
        name: имя файла для ссылки
        sem: семафор

    """
    async with aiohttp.ClientSession() as session:
        async with sem, session.get(link) as response:
            data_for_entries = await response.text()
            async with aiofiles.open(
                temporary_directory_path + name, 'w',
            ) as file:
                await file.write(data_for_entries)


def get_list_files():
    """Получение файлов из каталога.

    Returns:
        list_files (list): список файлов
    """
    list_files = []
    for root, _, files in os.walk(temporary_directory_path):
        for path_file in files:
            list_files.append(f'{root}/{path_file}')
    return list_files


def get_hash():
    """Вычисление хеша файлов.

    Returns:
        list_hash (list): список вычисленых хешей SHA-256
    """
    list_hash = []
    for path_file in get_list_files():
        with open(path_file, 'rb') as path_file:
            sha256_hash = hashlib.sha256()
            while True:
                data = path_file.read(SIZE)
                if not data:
                    break
                sha256_hash.update(data)
            list_hash.append(sha256_hash.hexdigest())

    return list_hash


async def main():
    """
    Функция обьединяющая всю логику модуля.

    Returns:
        get_hash() (list): список вычисленных хешей
    """
    sem = asyncio.BoundedSemaphore(NUMBER_OF_TREADS)
    list_name_for_urls = await asyncio.gather(
        asyncio.create_task(download_list_name_file(url_list_file)),
    )

    list_urls = []
    for name in list_name_for_urls[0]:
        list_urls.append(url + name)

    await asyncio.gather(
        *[
            asyncio.create_task(
                download_file(url_file, url_file.split('/')[-1], sem),
            )
            for url_file in list_urls
        ],
    )
    return get_hash()


if __name__ == '__main__':
    asyncio.run(main())
