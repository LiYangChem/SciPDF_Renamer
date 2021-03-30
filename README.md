# SciPDF_Renamer
# Introduction简介：
Auto rename new scientific literature PDF files based on its DOIs(auto search DOIs in metadat and pages) 
自动搜索DOI并重命名文献PDF文件

命名格式：abbreviated_journal_name year, volume, page+filename.pdf 

		例如：J. Am. Chem. Soc. 2006.128,2510-2511-非天然肽类.pdf
		
# 安装：

1.安装Python 3.6.8版本
2.运行“安装SciPDF_Renamer.bat”安装所需依赖

# 运行：
1.运行Run_watchdog.bat文件将会对该文件夹进行自动监控，并重命名新文件
2.如需对已存在的文件进行处理，请运行“Rename_All_pdf_in_folder.bat”
