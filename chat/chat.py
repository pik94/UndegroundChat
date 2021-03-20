import abc
import asyncio
from asyncio.streams import StreamReader, StreamWriter
import logging
from typing import Optional, Tuple


from chat.utils import set_logger_settings


logger = logging.getLogger(__file__)


class Chat(abc.ABC):
    def __init__(self,
                 host: str,
                 port: int,
                 log_file: Optional[str] = ''):
        self.host = host
        self.port = port

        set_logger_settings(log_file=log_file)

    async def connect_to_chat(self) -> Tuple[StreamReader, StreamWriter]:
        reader, writer = await asyncio.open_connection(self.host, self.port)
        return reader, writer

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        pass
