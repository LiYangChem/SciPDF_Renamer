@echo off 
rem 可以直接拖入文件
echo *********Add DOI to PDF MetaData****************
echo Listing the contents of %1
echo 请输入对应DOI号：
set /p doi=DOI is:
python AddMeta.py %1 %doi%
echo Add DOI completed 
echo *********Rename PDF from New MetaData****************
python PDFRenamer.py %1
echo Rename completed 
pause
 