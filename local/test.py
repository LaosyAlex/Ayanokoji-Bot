import compression
import asyncio

async def main():
    duration, width, height, FPS = await compression._get_video_info("C:\\Users\\phomm\\Downloads\\【TAB譜】一途 King Gnu ギター 弾いてみた [zV5S0_zkzvA].webm")

    print(f"{duration} + {width} + {height} + {FPS}")

asyncio.run(main())