"""All this is meant to work only on Windows.

logic:
all the files are set to copy.
those already copied are skipped by robocopy
if they are older than 24h and they have the same sizes and they have the same check sums, they will be deleted.

"""

import argparse
import logging
import os
from pathlib import Path
from platform import system
import sys
from urllib.error import URLError

from syncFiles.syncFiles import age, copy, check_sum, sizes_aggree
from syncFiles.sender import Sender, get_current_ip
from syncFiles.iterators import iter_chunks

DEBUG = True

# currentIP = get_current_ip()
server_ip = '192.168.1.100'
currentIP = '127.0.1.1' if (DEBUG and system() == "Linux") else server_ip

default_logs_folder = r"C:\Logs\sync.log" if system() == 'Windows' else "~/Logs/sync.log"


ap = argparse.ArgumentParser(description='Sync files between folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=r"Example: python syncFiles.py C:\test\V*.raw V:\RAW_test")
ap.add_argument('source_pattern', 
                type=Path,
                help='Pattern of the files to sync.')
ap.add_argument('target_folder', 
                type=Path, 
                help='Path to the folder that')
ap.add_argument("--check_sums", help="Check sums of files before and after copying.",
                action="store_true")
ap.add_argument('--min_copy_hours', 
                type=float,
                help='Minimal age in hours for the files to be copied.',
                default=4)
ap.add_argument('--min_delete_hours', 
                type=float,
                help='Minimal age in hours for the files to be deleted.',
                default=24)
ap.add_argument('--logs_path',
                type=lambda p: Path(p).expanduser().resolve(), 
                help='Where to save logs.',
                default=default_logs_folder)
ap.add_argument('--server_ip', 
                type=str, 
                help='IP of the server',
                default=currentIP)
ap.add_argument('--server_port', 
                type=int, 
                help='Port the server is listenning unto.',
                default=9001)
ap.add_argument('--message_encoding', 
                type=str, 
                help='Way the messages are encoded. Defaults to the one used on Windows.',
                default='cp1251')
ap.add_argument('--chunks',
                type=int,
                help='How many data-sets to sync at once?',
                default=16)
ap = ap.parse_args()


ap.logs_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=ap.logs_path,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('syncFiles.py')

log.info(f"LOGGED IN AS USER: {os.getlogin()}")
log.info(f"copy from: {ap.source_pattern} to: {ap.target_folder}")

target_folder = ap.target_folder
source_folder = ap.source_pattern.parent
pattern = ap.source_pattern.name 

all_files_to_copy = [f for f in source_folder.glob(pattern) if age(f, 'h') >= ap.min_copy_hours]

if not all_files_to_copy:
    log.error(f"No files matching pattern {ap.source_pattern} that are older than {ap.min_copy_hours}h.")
else:
    names_with_age = [f.name+f'that is {age(f,"h")}h old' for f in all_files_to_copy]
    log.info(f"Will try to copy: {' '.join(names_with_age)}")

    check_sums = ap.check_sums
    if ap.check_sums:
        sender = Sender(ap.server_ip, ap.server_port, ap.message_encoding)
        if not sender.connected:
            err = f"Failed to connect to {ap.server_ip}:{ap.server_port}. Proceeding without checking sums."
            log.error(err)
            check_sums = False

    for files_chunk in iter_chunks(all_files_to_copy, ap.chunks):
        copy(source_folder, target_folder, *[f.name for f in files_chunk])
        log.info("checking files and deleting wann alles stimmt.")
        for sf in files_chunk:
            file_age = age(sf, 'h')
            log.info(f"File {sf} is {file_age}h old.")
            if file_age >= ap.min_delete_hours:
                log.info(f"File {sf} is older than {ap.min_delete_hours}h")
                tf = target_folder/sf.name
                ok_to_delete = False
                try:
                    if sizes_aggree(sf, tf):
                        log.info(f"File sizes aggree: {sf} {tf}")
                        if check_sums:
                            s_check_sum = check_sum(sf)
                            t_check_sum = sender.get_check_sum(tf.name)
                            if s_check_sum == t_check_sum:
                                log.info(f"Check sums aggree: {sf} {tf}")
                                ok_to_delete = True
                            else:
                                log.error(f"Check sums differ: {sf} {tf}")
                        else:
                            ok_to_delete = True
                        if ok_to_delete:
                            log.info(f"Deleting {sf}")
                            try:
                                sf.unlink()
                            except PermissionError as e:
                                log.error(repr(e))
                            if sf.exists():
                                log.error(f"Could not delete: {sf}. Will repeat it in 24h.")
                    else:
                        log.error(f"Files sizes differ: {sf} {tf}")
                except FileNotFoundError:
                    log.error(f"Target file missing: {tf}")
            else:
                log.info(f"File {sf} is too young to delete.")

log.info('syncyWincy finished.')