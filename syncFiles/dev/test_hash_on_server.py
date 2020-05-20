from pathlib import Path

from syncFiles.syncFiles import check_sum, age, get_size_in_kilobytes


p = Path(r'V:\RAW\V200331_14.raw')
p.exists()

%%time
hs = check_sum(p,  chunksize=33554432)

%%time
age(p)

%%time
get_size_in_kilobytes(p)




p = Path(r'C:\Projects\cp\real')
list(p.glob('V*.raw'))

for f in p.glob('V*.raw'):
	print(age(f, 'h'))




