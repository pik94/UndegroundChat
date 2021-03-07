import argparse
import asyncio
from asyncio.streams import StreamReader, StreamWriter
import datetime as dt
from pathlib import Path
from typing import NoReturn, Tuple

import aiofiles


READ_SIZE = 1024


async def connect_to_chat(host: str,
                          port: int) -> Tuple[StreamReader, StreamWriter]:
    reader, writer = await asyncio.open_connection(host, port)
    return reader, writer


async def run(host: str, port: int, history_path: Path) -> NoReturn:
    reader, writer = await connect_to_chat(host, port)

    try:
        while True:
            data = await reader.read(READ_SIZE)
            date = dt.datetime.utcnow()
            async with aiofiles.open(history_path, 'a') as file:
                msg = f'[{date.strftime("%Y.%m.%d %H:%M")}] {data.decode()}'
                await file.write(msg)
    finally:
        writer.close()


def main(args: argparse.Namespace) -> NoReturn:
    host = args.host
    port = args.port
    history = Path(args.history)
    asyncio.run(run(host, port, history))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        type=str,
                        required=False,
                        default='minechat.dvmn.org',
                        help='A host of the server which you want to connect')
    parser.add_argument('--port',
                        type=int,
                        required=False,
                        default=5000,
                        help='A port of the server which you want to connect')
    parser.add_argument('--history',
                        type=str,
                        required=False,
                        default='history.txt',
                        help='A file where you want to save history.')
    args = parser.parse_args()
    main(args)
