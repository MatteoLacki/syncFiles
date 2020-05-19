"""All this is meant to work only on Windows."""
import os
from pathlib import Path
import subprocess
import time
import hashlib


def age(file_path, unit='h'):
    assert unit in ('s','h')
    age_in_s = time.time() - os.path.getctime(file_path)
    if unit == 's':
        return age_in_s
    else:
        return age_in_s/3600


def get_size_in_kilobytes(file_path):
    return os.path.getsize(file_path)


def copy(source, target, *file_names):
    """Copy files with Robocopy.exe.

    /is copies files  if they do not differ.
    """
    assert len(file_names) > 0, "Specify file names to copy."
    cmd = f"robocopy {str(source)} {str(target)} {' '.join(file_names)} /is"
    return subprocess.run(cmd.split()).returncode


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

