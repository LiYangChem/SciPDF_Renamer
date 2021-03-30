@echo off 
rem *********使用说明******************
echo 搜索PDF内的DOI信息，并对其规范化重命名
rem **********************

setlocal EnableDelayedExpansion

rem  定义文件夹
set pathstr=%~dp0

rem 设置变量k用于统计当前处理文件数目

set count = 0

::指定起始文件夹
set DIR="%cd%"

:: 括号中是通配符,可以指定后缀名,*.*表示所有文件
for /R %DIR% %%i in (*.pdf*) do ( 
set /a count =!count!+1
echo %%i
set lnm = %%i
python PDFRenamer.py "%%i"
echo 
)

echo Rename completed 
pause