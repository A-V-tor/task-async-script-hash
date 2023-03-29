from async_script_hash.main import *
import pytest


@pytest.mark.asyncio
async def test_download_list_name_file():
    assert len(await download_list_name_file(url_list_file)) == 10


@pytest.mark.asyncio
async def test_main():
    assert len(await main()) == 10


def test_get_hash():
    assert len(get_hash()) == 10