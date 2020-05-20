from syncFiles.sender import Sender, get_current_ip
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import socket


sender = Sender('0.0.0.0', '9001', 'cp1251')
sender.connected

sender = Sender('192.168.1.100', '9001', 'cp1251')
sender.connected

