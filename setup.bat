@echo off

copy /y bin\tidy.dll %windir%\System32
regsvr32 /s tidy.dll

python setup.py install
python bin\tagterm include etc res
