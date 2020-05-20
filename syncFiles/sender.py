from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import socket


def get_current_ip():
    return socket.gethostbyname(socket.gethostname())


class Sender(object):
    """A class used to simplify connections with the server."""
    def __init__(self,
                 host,
                 port=9001, 
                 encoding="cp1251"):
        self.host = host
        self.port = port
        self.encoding = encoding
        self.ip = socket.gethostbyname(socket.gethostname())

    def __sock(self, route, message=None):
        url = f"http://{self.host}:{self.port}/{route}"
        request = Request(url)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        if message is None:
            message = json.dumps(self.name).encode(self.encoding)
        return urlopen(request, message)

    def get_check_sum(self, relative_file_path, **check_sum_kwds):
        """Get the check sum for the file on the server.

        Args:
            relative_file_path (str): relative file path, w.r.t. the folder things are copied into.
        Returns:
            str: requested check sum.
        """
        message = json.dumps((str(relative_file_path), check_sum_kwds)).encode(self.encoding)
        with self.__sock('check', message) as s:
            check_sum = json.loads(s.read())
        return check_sum
