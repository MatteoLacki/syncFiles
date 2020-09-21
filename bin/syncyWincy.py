"""All this is meant to work only on Windows (surprise!).
I really tried using rsync, but Windows sucks, even with cygwin.

All files should copy.
Those already copied are skipped by robocopy
If they are older than 24h and they have the same sizes and they have the same check sums, they will be deleted.
"""
import argparse
import logging
import os
from pathlib import Path
from platform import system
from urllib.error import URLError
from pprint import pprint
import sys

from syncFiles.syncFiles import age as get_age, copy, check_sum, sizes_aggree
from syncFiles.sender import Sender, get_current_ip
from syncFiles.iterators import iter_chunks

DEBUG = True
#----------------------------------------------------- Defaults
server_port = '9001'
server_ip = '127.0.1.1' if (DEBUG and system() == "Linux") else '192.168.1.100'
#----------------------------------------------------- Input parsing
ap = argparse.ArgumentParser(description='Sync files between folders [wrapper aroud robocopy].',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=r"Example: python syncFiles.py C:\test V:\test *.raw --check_sums")
ap.add_argument("source",
                type=Path,
                help="The folder to copy from.")
ap.add_argument('target',
                type=Path,
                help='The folder to sync to.')
ap.add_argument('paths',
                type=Path,
                nargs='+',
                help='Files/folders to sync. If a folder is supplied, recursive copy will be executed.')
ap.add_argument("--check_sums",
                help="Check sums of files before and after copying.",
                action="store_true")
ap.add_argument('--min_copy_hours', 
                type=float,
                help='Minimal age in hours for the file to be copied. For a folder, the age of the youngest file within.',
                default=4)
ap.add_argument('--min_delete_hours', 
                type=float,
                help='Minimal age in hours for the file to be deleted. For a folder, the age of the youngest file within.',
                default=24)
ap.add_argument('--max_copy_trials', 
                type=int,
                help='Maximal number of copy trials for a file.',
                default=3)
ap.add_argument('--logs_path',
                type=lambda p: Path(p).expanduser().resolve(), 
                help='Where to save logs.',
                default=r"C:\Logs\sync.log" if system() == 'Windows' else "~/Logs/sync.log")
ap.add_argument('--server', 
                type=str, 
                help='IP:PORT of the server that checks the sums.',
                default=f"{server_ip}:{server_port}")
ap.add_argument('--message_encoding', 
                type=str, 
                help='Way the messages are encoded. Defaults to the one used on Windows.',
                default='cp1251')
ap.add_argument('--chunks',
                type=int,
                help='How many data-sets to sync at once?',
                default=16)
ap = ap.parse_args()
if DEBUG:
    pprint(ap.__dict__)
#----------------------------------------------------- Logging
ap.logs_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=ap.logs_path,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
log = logging.getLogger('syncFiles.py')
log.info(f"LOGGED IN AS USER: {os.getlogin()}")
log.info(f"copy from: {ap.sources} to: {ap.target}")

#----------------------------------------------------- Setting 'same_checksums'
same_checksums = lambda x,y: True
if ap.check_sums:
    ip, port = ap.server.split(':') if ':' in ap.server else (ap.server, server_port) 
    sender = Sender(ip, port, ap.message_encoding)
    if sender.connected:
        same_checksums = lambda sf, tf: check_sum(sf) == sender.get_check_sum(tf.name)
    else:
        log.error(f"Failed to connect to {ap.server}. Not checking sums.")

def properly_copied(p):
    """Check if files were correctly copied."""
    return sizes_aggree(ap.source/p, ap.target/p) and same_checksums(ap.source/p, ap.target/p)
#----------------------------------------------------- Copying

def iter_group_paths_age(paths):
    """Basic unit: root path and subpaths."""
    for p in paths:
        if p.is_dir():
            subpaths = list(p.rglob('*'))
            min_age = min(get_age(sp) for sp in subpaths)
            yield subpaths, min_age
        if p.is_file():
            yield group, [p], get_age(p)

for group, paths, age in iter_group_n_age(ap.paths):
    # check if qualifies to copy
    if age < ap.min_copy_hours:
        log.info(f"Age of group {group} is less than {ap.min_copy_hours}h: not copying.")
        continue
    # tryint to copy a given number of times
    copy_trial = 0
    while paths_to_copy and copy_trial < ap.max_copy_trials:
        copy(ap.source, ap.target, paths_to_copy)
        paths_to_copy = [p for p in paths_to_copy if not properly_copied(p)]
        copy_trial += 1
    if copy_trial == ap.max_copy_trials:
        log.error(f"Could not copy: {' '.join(paths_to_copy)}, even after trying {ap.max_copy_trials} times: repeat in 24h.")
        continue
    # check if qualifies to delete
    if age < ap.min_delete_hours:
        log.info(f"Age of group {group} is less than {ap.min_delete_hours}h: not deleting.")
        continue
    # deleting
    try:
        for p in paths: p.unlink()
    except Exception as e:
        log.error(f"{repr(e)}\nGroup {group} not copied.")
    else:
        log.info(f"Group {group} copied successfully.")


log.info('syncyWincy finished.')