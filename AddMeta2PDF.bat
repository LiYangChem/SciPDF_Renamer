@echo off 
rem ����ֱ�������ļ�
echo *********Add DOI to PDF MetaData****************
echo Listing the contents of %1
echo �������ӦDOI�ţ�
set /p doi=DOI is:
python AddMeta.py %1 %doi%
echo Add DOI completed 
echo *********Rename PDF from New MetaData****************
python PDFRenamer.py %1
echo Rename completed 
pause
 