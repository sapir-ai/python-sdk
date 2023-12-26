import argparse
import io
import logging
import os
from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable, BinaryIO, Type

from torch import load

from .manager import InferenceManager


class Action(Enum):
    Run = 1


def construct_server_class(handle: Callable[[BinaryIO, BinaryIO], str],
                           ) -> Type[BaseHTTPRequestHandler]:

    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path == "/":
                self.handle_request()

        def handle_request(self):
            logging.debug("start handling requests")
            content_length = int(self.headers.get('Content-Length', 0))
            request_body = self.rfile.read(content_length)

            response_body = io.BytesIO()
            content_type = handle(io.BytesIO(request_body), response_body)
            response_body.seek(0)

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(response_body.read())
            logging.debug("end handling requests")

    return SimpleHTTPRequestHandler


class InferenceAdapter:
    def __init__(self, manager: InferenceManager) -> None:
        self.__manager = manager

        self.__state_dict_path = os.environ.get('SAPIR_STATE_DICT_PATH')

    def start(self) -> None:
        action, argv = self.__parse_default_args()
        if action == Action.Run:
            self.__run(argv)
        else:
            raise NotImplementedError("unknown action %s" % action)

    def __run(self, argv: list[str]) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--port', '-p', default=8080)
        args = parser.parse_args(argv)

        logging.debug('start loading state dict')
        self.__manager.load_state_dict(load(self.__state_dict_path))
        logging.debug('end loading state dict')

        logging.info('start server')
        server_class = construct_server_class(self.__manager.handle)
        HTTPServer(('', args.port), server_class).serve_forever()
        logging.info('end server')

    @staticmethod
    def __parse_default_args() -> tuple[Action, list[str]]:
        parser = argparse.ArgumentParser()
        parser.add_argument('action', type=Action)
        parser.add_argument('--log-level', '-ll',
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                     'CRITICAL'])
        args, argv = parser.parse_known_args()

        logging.basicConfig(level=getattr(logging, args.log_level),
                            format='%(asctime)s\t%(levelname)s\t%(message)s')

        return args.action, argv
