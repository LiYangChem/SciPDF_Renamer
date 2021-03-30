import sys 
# assigns 'os' to global namespace
from os import path
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.generic import NameObject, createStringObject


def rename(pdf,doi):
    #inpfn = 'Chem. Rev. 2019, 119, 10241-10287-VIP-acs.chemrev.9b00008.pdf'
 

    fin = open(pdf, 'rb')
    pdf_in = PdfFileReader(fin)

    writer = PdfFileWriter()

    for page in range(pdf_in.getNumPages()):
        writer.addPage(pdf_in.getPage(page))

    infoDict = writer._info.getObject()

    info = pdf_in.documentInfo
    for key in info:
        infoDict.update({NameObject(key): createStringObject(info[key])})
        print(key[0]+':'+ info[key])

    # add the grade
    infoDict.update({NameObject('/doi'): createStringObject(u''+doi)})

    # It does not appear possible to alter in place.
    temppdf=pdf+'.temppdf'
    fout = open(temppdf, 'wb')


    writer.write(fout)


    fin.close()
    fout.close()

 
    import os
    os.unlink(pdf)
    os.rename(temppdf, pdf)
    print('The DOI have been updated to:{0}'.format(doi))
if __name__ == '__main__':
    #try:
        rename(sys.argv[1],sys.argv[2] )
   # except:
    #    print('Error Get!')