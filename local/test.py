from youtube import Youtube
import asyncio

test = Youtube("https://www.youtube.com/watch?v=SE1Z1-rJoB4")

asyncio.run(test._download("https://www.youtube.com/watch?v=SE1Z1-rJoB4"))

             