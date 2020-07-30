import asyncio
import aiohttp
import time
import sys

async def fetch(url, session):
    print(f'fetching: {url}')
    async with session.get(url) as response:
        if response.headers['Content-Type'] == "application/json":
            print(f'Done fetching: {url}')
            return await response.json()
        return f"Could not get json data: {url}"


async def main(file):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in open(f'{file}').readlines():
            task = asyncio.create_task(fetch(url, session))
            tasks.append(task)
    res = await asyncio.gather(*tasks, return_exceptions=False)
    print(res)

if __name__ == "__main__":
    t = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv[1]))
    loop.close()
    t2 = time.perf_counter() - t
    print(f'process took {t2:0.2f} seconds')
