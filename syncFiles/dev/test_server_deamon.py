from syncFiles.sender import Sender, get_current_ip
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import socket
from pathlib import Path

from syncFiles.syncFiles import check_sum


#9001
sender = Sender('0.0.0.0', '9001', 'cp1251')
sender = Sender('192.168.1.100', '9001', 'cp1251')
sender.connected




%%time
remote_check_sum = sender.get_check_sum('V210401_01.raw')
local_V200310_10 = check_sum("V:/RAW/V210401_01.raw")

local_V200310_10 == remote_check_sum
