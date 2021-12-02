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


# class Network:
#     def __init__(self, headers: dict):
#         self.session = aiohttp.ClientSession(headers=headers)
#
#     async def _get_response(self, url: str, json: bool):
#         async with self.session.get(url) as resp:
#             if resp.status != 200:
#                 return None
#             return resp.json() if json else resp.text()
#
#     async def get_response(self, url: str, json: bool = True):
#         return await self._get_response(url, json)
#
#     async def get_responses(self, urls: dict):
#         tasks: list = []
#
#         for url, json in urls.items():
#             tasks.append(asyncio.ensure_future(self._get_response(url, json)))
#
#         results: list = await asyncio.gather(*tasks)
#         return results
