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

    def run(self, log_level: Optional[int] = logging.INFO):
        logger.setLevel(log_level)
        logger.info('Type your messages:')
        while True:
            message = input()
            logger.info(message)
            asyncio.run(self.write(message))

    async def write(self, message: str):
        reader, writer = await asyncio.open_connection(self.host, self.port)

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
                chat_welcome_msg = data[0]
            elif len(data) > 3:
                metadata = data[1]
                chat_welcome_msg = data[1]
            else:
                logger.debug('Exit')
                writer.close()
                return

            logger.debug(chat_welcome_msg)
            if metadata == 'null':
                logger.debug('Input account hash is not valid.')
                writer.close()
                return

            if not message.endswith('\n'):
                message = f'{message}\n'

            logger.debug('Send your message to chat...')
            writer.write(f'{message}\n'.encode())
            logger.debug('Success!')
        except Exception as e:
            logger.debug('Something was wrong!')
            logger.debug(e)
        finally:
            writer.close()
