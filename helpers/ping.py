from ping3 import ping
import asyncio

async def do_ping(host) -> str:   # i dont understand this code right nnw
    result = await asyncio.to_thread(lambda : ping(host)*1000)
    if result:
        return f"{result:.2f}"
    else:
        return "Timed Out"