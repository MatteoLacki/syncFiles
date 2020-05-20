"""All this is meant to work only on Windows."""
import argparse
import logging
from pathlib import Path
from platform import system
import sys

from syncFiles.syncFiles import age, copy, check_sum, sizes_aggree
from syncFiles.sender import Sender, get_current_ip

DEBUG = True

currentIP = get_current_ip()
if DEBUG and system() == "Linux":
    currentIP = '127.0.1.1'


default_logs_folder = r"C:\Logs\sync.log" if system() == 'Windows' else "~/Logs/sync.log"


ap = argparse.ArgumentParser(description='Sync files between folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=r"Example: python syncFiles.py C:\test\V*.raw V:\RAW_test")
ap.add_argument('source_pattern', 
                type=lambda p: Path(p).expanduser().resolve(),
                help='Pattern of the files to sync.')
ap.add_argument('target_folder', 
                type=Path, 
                help='Path to the folder that')
ap.add_argument("--check_sums", help="Check sums of files before and after copying.",
                action="store_true")
ap.add_argument('--min_age_hours', 
                type=float,
                help='Minimal age in hours for the files to be copied.',
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
ap = ap.parse_args()


ap.logs_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=ap.logs_path,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:')
log = logging.getLogger('syncFiles.py')


log.info("copying files")
log.info("FROM: " + str(ap.source_pattern))
log.info("TO: " + str(ap.target_folder))
log.info("How old are files in hours?: " + str(ap.target_folder))


target_folder = ap.target_folder
source_folder = ap.source_pattern.parent
pattern = ap.source_pattern.name 

if DEBUG:
    print(ap.logs_path)
    print(ap.source_pattern)
    print(ap.min_age_hours)
    for f in source_folder.glob(pattern):
        print(f"File {f} is {age(f,'h')} h old.")


old_files = [f for f in source_folder.glob(pattern) if age(f, 'h') >= ap.min_age_hours]
file_names = [f.name for f in old_files]
if not file_names:
    err = f"no files matching pattern {ap.source_pattern}"
    log.error(err)
    sys.exit(err)

if ap.check_sums:
    sender = Sender(ap.server_ip, ap.server_port, ap.message_encoding)

log.info(f"files older than {ap.min_age_hours} hours: {' '.join([str(f) for f in old_files])}")
copy(source_folder, target_folder, *file_names)

log.info("checking files and deleting wann alles stimmt.")
for sf in old_files:
    tf = target_folder/sf.name
    try:
        if sizes_aggree(sf, tf):
            log.info(f"File sizes aggree: {sf} {tf}")
            if ap.check_sums:
                s_check_sum = check_sum(sf)
                t_check_sum = sender.get_check_sum(tf.name)
                if s_check_sum == t_check_sum:
                    log.info(f"Check sums aggree: {sf} {tf}")
                    log.info(f"Deleting {sf}")
                    sf.unlink()
                else:
                    log.error(f"Check sums differ: {sf} {tf}")
            else:
                log.info(f"Deleting {sf}")
                sf.unlink()
        else:
            log.error(f"Files sizes differ: {sf} {tf}")
    except FileNotFoundError:
        log.error(f"Target file missing: {tf}")
