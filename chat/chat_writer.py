import asyncio
import logging
from typing import Optional

from chat.chat import Chat

logger = logging.getLogger(__file__)


class ChatWriter(Chat):
    def __init__(self,
                 host: str,
                 port: int,
                 account_hash: str,
                 log_file: Optional[str] = 'chat_writer.log',
                 read_size: Optional[int] = 1024):
        self.account_hash = account_hash
        self.read_size = read_size

        super().__init__(host, port, log_file)

    def run(self,
            message: str,
            log_level: Optional[int] = logging.INFO):
        logger.setLevel(log_level)
        asyncio.run(self.write(message))

    async def write(self, message: str):
        reader = await self.reader
        writer = await self.writer

        try:
            data = await reader.read(self.read_size)
            data = data.decode('utf-8')
            logger.debug(data)
            writer.write(f'{self.account_hash}\n'.encode())

            await asyncio.sleep(2)
            data = await reader.read(self.read_size)
            data = data.decode().split('\n')
            if len(data) == 3:
                metadata = data[0]
            else:
                metadata = data[1]

            if metadata == 'null':
                return

            logger.info('Send your message to chat...')

            if not message.endswith('\n'):
                message = f'{message}\n'

            writer.write(f'{message}\n'.encode())
            logger.info('Success!')
        except:
            logger.info('Something was wrong!')
        finally:
            writer.close()