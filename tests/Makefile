clean:
	touch V1.raw
	touch V2.raw
	touch V3.raw
	touch V4.raw
	touch V5.raw
	touch V6.raw
	touch V7.raw
	touch V8.raw
	touch V9.raw
	touch V10.raw
	touch V11.raw
	touch V12.raw
	touch V13.raw
	touch V14.raw
	touch V15.raw
	mkdir -p s
	mkdir -p t
	rm s/* || true
	rm t/* || true
	mv *.raw s
testrun:
	syncyWincy.py 's/*.raw' t --min_copy_hours=.0001 --check_sums
dummytimsdata:
	mkdir -p tims.d
	touch tims.d/analysis.tdf
	touch tims.d/analysis.tdf_bin
	touch tims.d/BackgroundLinePos.ami
	touch tims.d/BackgroundProfPos.ami
	touch tims.d/chromatography-data-pre.sqlite
	touch tims.d/chromatography-data.sqlite-journal
	touch tims.d/configuration.hss
	touch tims.d/DensViewPos.ami
	touch tims.d/DensViewPosBgnd.ami
	touch tims.d/desktop.ini
	mkdir -p tims.d/blah
	touch tims.d/blah/column_setpoint.txt
	touch tims.d/blah/column_temprature.txt
	touch tims.d/blah/execution-log.txt
	touch tims.d/blah/flowsensor-a_flow.txt
	touch tims.d/blah/flowsensor-b_flow.txt
	mkdir -p timses
	mv tims.d timses/tims1.d
	cp -r timses/tims1.d timses/tims2.d
	cp -r timses/tims1.d timses/tims3.d
	cp -r timses/tims1.d timses/tims4.d
	cp -r timses/tims1.d timses/tims5.d

