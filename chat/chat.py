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

        self._reader = None
        self._writer = None

    @property
    async def reader(self) -> StreamReader:
        if self._reader is None:
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port)
        return self._reader

    @property
    async def writer(self) -> StreamWriter:
        if self._writer is None:
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port)
        return self._writer

    async def connect_to_chat(self) -> Tuple[StreamReader, StreamWriter]:
        reader, writer = await asyncio.open_connection(self.host, self.port)
        return reader, writer

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        pass
