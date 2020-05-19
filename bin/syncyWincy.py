"""All this is meant to work only on Windows."""
import argparse
import logging
from pathlib import Path
import sys

from syncFiles.syncFiles import age, copy, check_sums_aggree, sizes_aggree


ap = argparse.ArgumentParser(description='Sync files between folders.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                             epilog=r"Example: python syncFiles.py C:\test\V*.raw V:\RAW_test")
ap.add_argument('source_pattern', 
                type=Path, 
                help='Pattern of the files to sync.')
ap.add_argument('target_folder', 
                type=Path, 
                help='Path to the folder that')
ap.add_argument('--min_age_hours', 
                type=float, 
                help='Minimal age in hours for the files to be copied.',
                default=24)
ap.add_argument('--logs_path', 
                type=Path, 
                help='Where to save logs.',
                default=r"C:\Logs\sync.log")
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

old_files = [f for f in source_folder.glob(pattern) if age(f, 'h') >= ap.min_age_hours]
file_names = [f.name for f in old_files]
if not file_names:
    err = f"no files matching pattern {ap.source_pattern}"
    log.error(err)
    sys.exit(err)
    

log.info(f"files older than {ap.min_age_hours} hours: {' '.join([str(f) for f in old_files])}")
copy(source_folder, target_folder, *file_names)

log.info("checking files and deleting wann alles stimmt.")
for sf in old_files:
    tf = target_folder/sf.name
    try:
        if sizes_aggree(sf, tf):
            log.info(f"File sizes aggree: {sf} {tf}")
            if check_sums_aggree(sf, tf):
                log.info(f"Check sums aggree: {sf} {tf}")
                log.info(f"Deleting {sf}")
                sf.unlink()
            else:
                log.error(f"Check sums differ: {sf} {tf}")
        else:
            log.error(f"Files sizes differ: {sf} {tf}")
    except FileNotFoundError:
        log.error(f"Target file missing: {tf}")
