import argparse
import logging
from typing import NoReturn

from chat import ChatWriter


def main(args: argparse.Namespace) -> NoReturn:
    host = args.host
    port = args.port
    account_hash = args.account_hash
    log = args.log
    chat_writer = ChatWriter(host, port, account_hash, log)
    if args.debug:
        chat_writer.run(logging.DEBUG)
    else:
        chat_writer.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug',
                        required=False,
                        action='store_true',
                        default=False,
                        help='Turn on a debug mode.')
    parser.add_argument('--host',
                        type=str,
                        required=False,
                        default='minechat.dvmn.org',
                        help='A host of the chat which you want to connect.')
    parser.add_argument('--port',
                        type=int,
                        required=False,
                        default=5050,
                        help='A port of the chat which you want to connect '
                             'to write messages.')
    parser.add_argument('--nickname',
                        type=str,
                        required=False,
                        default='Anonymous',
                        help='A nickname for the chat.')
    parser.add_argument('--account_hash',
                        type=str,
                        required=False,
                        default='',
                        help='An account hash to write messages to the chat.'
                        )
    parser.add_argument('--log',
                        type=str,
                        required=False,
                        default='chat_writer.log',
                        help='A log path.')
    args = parser.parse_args()
    main(args)
