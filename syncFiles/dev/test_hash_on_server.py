from pathlib import Path

from syncFiles.syncFiles import check_sum, age, get_size_in_kilobytes


p = Path(r'V:\RAW\V200331_14.raw')
p = Path(r"I:\RAW_OT\I210607_05.raw")
p.exists()


%%time
hs = check_sum(p,  chunksize=33554432)

%%time
age(p)

%%time
get_size_in_kilobytes(p)


age(r"D:\rawdata_test\I210608_70.raw")
