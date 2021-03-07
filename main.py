import asyncio
from asyncio.streams import StreamReader, StreamWriter
from typing import Tuple


async def connect_to_chat(host: str,
                          port: int) -> Tuple[StreamReader, StreamWriter]:
    reader, writer = await asyncio.open_connection(host, port)
    return reader, writer


async def run(host: str, port: int):
    reader, writer = connect_to_chat(host, port)

    try:
        while True:
            data = await reader.read(100)
            print(f'Received: {data.decode()}')
    finally:
        writer.close()


if __name__ == '__main__':
    host = 'minechat.dvmn.org'
    port = 5000
    asyncio.run(run(host, port))
