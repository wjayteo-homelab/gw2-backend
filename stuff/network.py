import asyncio

import aiohttp


async def _get_response(session, url: str, json: bool):
    async with session.get(url) as resp:
        if resp.status != 200:
            return None

        if json:
            return await resp.json()
        else:
            return await resp.text()


async def get_response(headers: dict, url: str, json: bool = True):
    async with aiohttp.ClientSession(headers=headers) as session:
        return await _get_response(session, url, json)


async def get_responses(headers: dict, urls: dict) -> list:
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks: list = []

        for url, json in urls.items():
            tasks.append(asyncio.ensure_future(_get_response(session, url, json)))

        results: list = await asyncio.gather(*tasks)
        return results
