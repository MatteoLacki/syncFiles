import os
from pathlib import Path
import subprocess
import time
import hashlib
from platform import system
import shutil


def age(file_path, unit='h'):
    """Get file age.

    Args:
        file_path (str): Path to file.
        unit (str): 's' for seconds, 'm' for minutes, 'h' for hours, 'd' for days."""
    age_in_s = time.time() - os.path.getctime(file_path)
    return {'s': age_in_s,
            'm': age_in_s/60,
            'h': age_in_s/3600,
            'd': age_in_s/86400 }[unit]


def get_size_in_kilobytes(file_path):
    """Get file size in kilobytes."""
    return os.path.getsize(file_path)


def robocopy(source, target, file_name_list=[], params='/is /it /r:10 /w:10 /mt /E /z'):
    """Copy files.
    
    /is copies same files:
    /it copies tweaked files.
    /mt multithreading
    /E include subdirectories.

    /COPY:DT /DCOPY:T preserve the date and time stamps.
    /COPY:DAT is default.

    check on: https://docs.microsoft.com/de-de/windows-server/administration/windows-commands/robocopy
    """
    cmd = f"robocopy {str(source)} {str(target)} {' '.join(file_name_list)} {params}"
    return subprocess.run(cmd.split()).returncode


def linuxcopy(source, target, file_name_list):
    if file_name_list:
        for fn in file_name_list:
            shutil.copy2(str(source/fn), str(target/fn))
    else:
        shutil.copytree(str(source), str(target))
    return 1


def copy(source, target, file_name_list=[], params='/is /it /r:10 /w:10 /mt /E'):
    return robocopy(source, target, file_name_list, params) if system()=='Windows' else linuxcopy(source, target, file_name_list)


def check_sum(file_path, algo=hashlib.blake2b, chunksize=8192):
    """algo (hashlib function): E..g hashlib.blake2b, hashlib.md5."""
    with open(file_path, "rb") as f:
        file_hash = algo()
        chunk = f.read(chunksize)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunksize)
    return file_hash.hexdigest()


def check_sums_aggree(file_name_0, file_name_1, **kwds):
    return check_sum(file_name_0, **kwds) == check_sum(file_name_1, **kwds)
        

def sizes_aggree(file_name_0, file_name_1):
    return get_size_in_kilobytes(file_name_0) == get_size_in_kilobytes(file_name_1)

