@echo off 
rem *********ʹ��˵��******************
echo ����PDF�ڵ�DOI��Ϣ��������淶��������
rem **********************

setlocal EnableDelayedExpansion

rem  �����ļ���
set pathstr=%~dp0

rem ���ñ���k����ͳ�Ƶ�ǰ�����ļ���Ŀ

set count = 0

::ָ����ʼ�ļ���
set DIR="%cd%"

:: ��������ͨ���,����ָ����׺��,*.*��ʾ�����ļ�
for /R %DIR% %%i in (*.pdf*) do ( 
set /a count =!count!+1
echo %%i
set lnm = %%i
python PDFRenamer.py "%%i"
echo 
)

echo Rename completed 
pause