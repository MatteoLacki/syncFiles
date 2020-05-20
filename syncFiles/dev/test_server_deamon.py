from syncFiles.sender import Sender, get_current_ip
from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import socket
from pathlib import Path

from syncFiles.syncFiles import check_sum


sender = Sender('0.0.0.0', '9001', 'cp1251')
sender.connected

sender = Sender('192.168.1.100', '9001', 'cp1251')
sender.connected

%%time
remote_check_sum = sender.get_check_sum('V200310_10.raw')

local_V200310_10 = Path(r"C:\Projects\cp\real")/'V200310_10.raw'

%%time
local_check_sum = check_sum(local_V200310_10)



local_check_sum == remote_check_sum