import asyncio
import datetime as dt
import logging
from pathlib import Path
from typing import Optional

import aiofiles

from chat.chat import Chat


logger = logging.getLogger(__file__)


class ChatReader(Chat):
    def __init__(self,
                 host: str,
                 port: int,
                 history_file: Optional[str] = 'chat.txt',
                 log_file: Optional[str] = 'chat_reader.log',
                 read_size: Optional[int] = 1024):
        self.history_file = Path(history_file)
        self.read_size = read_size

        super().__init__(host, port, log_file)

    def run(self, log_level: Optional[int] = logging.INFO):
        logger.setLevel(log_level)
        asyncio.run(self.read())

    async def read(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        try:
            while True:
                data = await reader.read(self.read_size)
                date = dt.datetime.utcnow()
                async with aiofiles.open(self.history_file, 'a') as file:
                    data = data.decode('utf-8')
                    msg = f'[{date.strftime("%Y.%m.%d %H:%M")}] {data}'
                    await file.write(msg)
        finally:
            writer.close()
