import logging
from logging.config import dictConfig
from pathlib import Path
from typing import NoReturn, Optional


def set_logger_settings(level: Optional[int] = logging.INFO,
                        log_file: Optional[str] = 'chat.log') -> NoReturn:
    handlers = {
        'console': {
            'class':        'logging.StreamHandler',
            'formatter':    'console',
        },
    }

    root_handlers = ['console']

    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(exist_ok=True, parents=True)
        handlers['file'] = {
            'class':        'logging.handlers.RotatingFileHandler',
            'formatter':    'detailed',
            'filename':     log_file,
            'mode':         'a',
            'maxBytes':     1048576,  # 1 MB
            'backupCount':  5
        }
        root_handlers.append('file')

    config = dict(
        version=1,
        formatters={
            # For files
            'detailed': {
                'format': '%(asctime)s %(levelname)-8s %(message)s'
            },
            # For the console
            'console': {
                'format': '%(asctime)s [%(levelname)s] %(message)s'}
        },
        handlers=handlers,
        root={
            'handlers': root_handlers,
            'level':    level,
        },
        disable_existing_loggers=False
    )
    dictConfig(config)
