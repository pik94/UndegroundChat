import asyncio
from asyncio.streams import StreamReader, StreamWriter
import datetime as dt
from pathlib import Path
from typing import Tuple

import aiofiles


READ_SIZE = 1024


async def connect_to_chat(host: str,
                          port: int) -> Tuple[StreamReader, StreamWriter]:
    reader, writer = await asyncio.open_connection(host, port)
    return reader, writer


async def run(host: str, port: int, chat_file: Path):
    reader, writer = await connect_to_chat(host, port)

    try:
        while True:
            data = await reader.read(READ_SIZE)
            date = dt.datetime.utcnow()
            async with aiofiles.open(chat_file, 'a') as file:
                msg = f'[{date.strftime("%Y.%m.%d %H:%M")}] {data.decode()}'
                await file.write(msg)
    finally:
        writer.close()


if __name__ == '__main__':
    host = 'minechat.dvmn.org'
    port = 5000
    chat_file = Path('chat.txt')
    asyncio.run(run(host, port, chat_file))
