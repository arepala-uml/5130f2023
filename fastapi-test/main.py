import asyncio
from collections.abc import Coroutine
from socket import AF_INET
from typing import List, Optional, Any, Dict

import aiohttp
from fastapi import FastAPI
from fastapi.logger import logger as fastAPI_logger  # convenient name
from fastapi.requests import Request
from fastapi.responses import Response
import uvicorn

SIZE_POOL_AIOHTTP = 100

class SingletonAiohttp:
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str) -> Any:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url) as response:
                if response.status != 200:
                    return {"ERROR OCCURED" + str(await response.text())}

                json_result = await response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result


async def on_start_up() -> None:
    fastAPI_logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()


app = FastAPI(docs_url="/", on_startup=[on_start_up], on_shutdown=[on_shutdown])

urls = ["https://google.com/",
        "https://bing.com/",
        "https://duckduckgo.com",
        "http://www.dogpile.com"]

@app.get('/endpoint_multi')
async def endpoint_multi() -> Dict[str, int]:
    url = "http://localhost:8080/test"
    async_calls: List[Coroutine[Any, Any, Any]] = list()  # store all async operations
    for url in urls:
        async_calls.append(SingletonAiohttp.query_url(url))
    # async_calls.append(SingletonAiohttp.query_url(url))

    all_results: List[Dict[Any, Any]] = await asyncio.gather(*async_calls)  # wait for all async operations
    for res in all_results:
        print(res)
    # {'success': sum([x['success'] for x in all_results])}
    return {}

async def fetch_url(session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    response = await session.get(url)
    return {'url': response.url, 'status': response.status}

async def async_get_urls_v2():
    """Asynchronously retrieve the list of URLs."""
    async with aiohttp.ClientSession as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url))
            tasks.append(task)
        sites = await asyncio.gather(*tasks)

    # Generate the HTML response
    response = '<h1>URLs:</h1>'
    for site in sites:
        response += f"<p>URL: {site['url']} --- Status Code: {site['status']}</p>"

    return response

@app.get('/asyncio')
async def read_results():
    results = await async_get_urls_v2()
    return results
