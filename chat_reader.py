import argparse
from pathlib import Path
from typing import NoReturn, Tuple

from chat import ChatReader


def main(args: argparse.Namespace) -> NoReturn:
    host = args.host
    port = args.port
    history = Path(args.history)
    log = args.log
    chat_reader = ChatReader(host, port, history, log)
    chat_reader.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        type=str,
                        required=False,
                        default='minechat.dvmn.org',
                        help='A host of the server which you want to connect.')
    parser.add_argument('--port',
                        type=int,
                        required=False,
                        default=5000,
                        help='A port of the server which you want to connect '
                             'to read messages.')
    parser.add_argument('--history',
                        type=str,
                        required=False,
                        default='history.txt',
                        help='A file where you want to save history.')
    parser.add_argument('--log',
                        type=str,
                        required=False,
                        default='chat_reader.log',
                        help='A log path.')
    args = parser.parse_args()
    main(args)
