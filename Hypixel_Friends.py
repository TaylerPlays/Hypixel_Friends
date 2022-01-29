import requests
import time
import asyncio
import aiohttp


start_time = time.time()

name = input("Enter a username: ")
response1 = requests.get(f'https://api.slothpixel.me/api/players/{name}/friends')
data = response1.json()
results = []
elements = []

for element in data:
    elements.append(element['uuid'])

def get_tasks(session):
    tasks = []
    for item in elements:
        tasks.append(session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{item}",ssl=False))
    return tasks


async def get_ign():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)
        for res in responses:
            data2 = await res.json()
            usernames = data2['name']
            results.append(usernames)


asyncio.run(get_ign())
listToStr = ' '.join(map(str, results)).replace(" ","\n")

print(listToStr)
print('-----------------------------')
print(len(results))

print("--- %s seconds ---" % (time.time() - start_time))