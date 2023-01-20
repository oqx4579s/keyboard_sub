import logging
import os
from enum import Enum
from threading import Thread
from typing import Optional

import zmq.auth
from django.conf import settings
from zmq.auth import thread
from zmq.auth.base import Authenticator
from zmq.sugar.context import Context
from zmq.sugar.socket import Socket

from keyboard_sub.subscriber.models import Log

logger = logging.getLogger()


class AuthenticationThread(thread.AuthenticationThread):
    def __init__(
            self,
            authenticator: Authenticator,
            pipe: zmq.Socket,
    ) -> None:
        super().__init__(authenticator, pipe)
        self.daemon = True


thread.AuthenticationThread = AuthenticationThread


class Status(Enum):
    ACTIVE = 'ACTIVE'
    STOP = 'STOP'


class Subscriber:
    def __init__(self):
        self.__auth: Optional[Authenticator] = None
        self.__socket: Optional[Socket] = None
        self.__context: Context = zmq.Context.instance()

        self.__thread: Optional[Thread] = None
        self._daemon: bool = True
        self.status: Status = Status.STOP

    def start(self):
        self._start()
        self.status = Status.ACTIVE
        self.__thread = Thread(target=self.__main_loop, name='Subscriber')
        self.__thread.daemon = self._daemon
        self.__thread.start()

    def shutdown(self):
        self.__thread.join(timeout=0)
        del self.__thread
        self.__auth.stop()
        self.__socket.close()

    def _start(self):
        public_keys_dir = os.path.join(settings.AUTH_KEYS_PATH, 'public_keys')
        secret_keys_dir = os.path.join(settings.AUTH_KEYS_PATH, 'private_keys')

        auth = thread.ThreadAuthenticator(self.__context)
        auth.start()
        auth.configure_curve(domain='*', location=public_keys_dir)

        self.__socket = self.__context.socket(zmq.SUB)

        client_secret_file = os.path.join(secret_keys_dir, 'client.key_secret')
        client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
        self.__socket.curve_secretkey = client_secret
        self.__socket.curve_publickey = client_public

        server_public_file = os.path.join(public_keys_dir, 'server.key')
        server_public, _ = zmq.auth.load_certificate(server_public_file)
        self.__socket.curve_serverkey = server_public

        self.__socket.connect(settings.SUB_SOCKET)
        self.__socket.subscribe('')

    def __main_loop(self):
        while self.status == Status.ACTIVE:
            self._save(self.__socket.recv_json())

    @staticmethod
    def _save(data_to_save: dict):
        log = Log.objects.get(id=Log.objects.create(**data_to_save).id)
        logger.info(f'Object {log} was created.')


subscriber = Subscriber()


