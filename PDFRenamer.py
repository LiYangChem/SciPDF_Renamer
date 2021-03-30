import PyPDF3, sys, argparse, requests,os,re
#cankao:https://github.com/pormr/DOIHelper/blob/master/DOIExtract.py
#https://gist.github.com/ipudu/b72031f84a0e6cfdf6626a791f8fe380
crossref = 'http://api.crossref.org/'
 
def rename(pdf):
    try:
        """Rename an academic article pdf file with human readable format
        
        Arguments:
            pdf {String} -- pdf file name
        """
        indicator='null'
        name='null'
        subj='null'
        doi='null'
        pdfname=os.path.basename(pdf)
        pdffullpath=os.path.abspath(pdf)
        pdffolder= os.path.dirname(pdffullpath)
        print(pdffullpath)
        print(pdffolder)
        pdfFileObj = open(pdf,'rb')

        pdfReader = PyPDF3.PdfFileReader(pdfFileObj)
        actiontxt=''
        #基于不同的文章类型尝试获取DOI和subject两个数据
        #优先按照DOI获取信息
        #try to find doi in metadata
        for k, v in pdfReader.documentInfo.items():
            print(k+': '+v)
            if 'doi' in k:
                actiontxt='doi'
                doi = v
                break
            elif 'WPS-ARTICLEDOI' in k:
                actiontxt='doi'
                doi = v
                break
            elif 'Subject' in k:
                actiontxt='Subject'
                subj=v
                #break
           
        print('-----------------------')
        print('action code:'+actiontxt)
        
        #if cant find doi in metadata then find it in full text url
        if doi=='null':# and (not actiontxt=='Subject'):     
            print('doi:'+doi)
            pages = pdfReader.getNumPages()
            print("is wrong?")
            print('Total page number: '+ str(pages) )
            key = '/Annots'
            uri = '/URI'
            anc = '/A'
            bib = []
            
            for page in range(pages):
                print("is wrong?")
                print(page.__index__)
                dois= dict()
                pageSliced = pdfReader.getPage(page)
                pageObject = pageSliced.getObject()
                doi_count=0
                #run only once, if find doi then stop
                if key in pageObject and (doi=='null'):
                    ann = pageObject[key]
                    for a in ann:
                        
                        u = a.getObject()
                        if anc in u and uri in u[anc]:
                            if "doi" in u[anc][uri]:
                                bib.append(u[anc][uri])
                                #get_doi(u[anc][uri])
                                print("DOI:"+u[anc][uri])
                                doi=u[anc][uri] 
                                if doi in dois:
                                    dois[doi]=dois[doi]+1
                                else:
                                    dois[doi]=1
                doi_count=len(dois)
                #如果出现三个以上的doi，那么说明此页是参考文献位置
                print('Find '+str(doi_count)+' dois on page-'+str(page))
                sorted_dois=sorted(dois.items(), key=lambda item: item[1], reverse=True)
                print('sorted the dict')
                if doi_count>4:
                    doi='null'
                    
                    print('Too many dois in one page-{0}, it\'s referenc page, drop it!'.format(doi_count))
                elif doi_count>0:
                    doi=next(iter(sorted_dois))[0]    
                    actiontxt='doi'
                    print(doi)
                    """patt='10.(\d)+/([^(\s\>\"\<)])+'
                    searchObj = re.search( patt, doi, re.M|re.I) 
                    if searchObj:
                        print ('searchObj.group() : '+ searchObj.group())
                    else:
                        print('searchObj.group() : null')
                   """
                    if '?' in doi:
                        urldoi=doi.split('?')
                        for urlpart in urldoi:
                            if '10' in urlpart:
                                doi=urlpart
                                break
                            
                    # this get err print(str(sorted_dois[doi]))
                    print('Find right doi on page-{0}, it\'s :{1}'.format(str(doi_count), doi ))
              
                    break
                else:
                    doi='null'
                    print('No doi found on page-{0}.'.format(str(doi_count)))

        #job done, 开始处理doi或者subject信息  
        #优先按照DOI获取信息
        pdfFileObj.close()
        if  doi=='null':
            name='null'
            print('No doi found in this document')
            print('*************************************')
            indicator='null'
            if actiontxt=='Subject':
                print('Found subject for this document:'+subj)  
                name=subj.replace(':',',')
                indicator=name.split(',')[1]   
        else:# actiontxt=='doi':
            #优先doi检查，因为之前的都是doi，使用doi结果查重
            print('Found doi for this document:'+doi)
        
            url = '{}works/{}'.format(crossref, doi)
            print(url)
            r = requests.get(url)
            print("Http status code："+str(r.status_code))
            #print(r.text)
            if str(r.status_code)=="200":
                item = r.json()
                print("Data been serialized:")
                # no error handlings and will not work for very new articles
                try:
                    #Json返回值各不相同,Check if key avaluable in JSON
                    
                    if "short-container-title" in item:
                        abbreviated_journal = item['message']['short-container-title'][0]
                    elif "container-title" in item['message']:
                        abbreviated_journal = item['message']["container-title"][0]
                 


                    year = item['message']['created']['date-parts'][0][0]
                    volume = item['message']['volume']
                    page = item['message']['page']
                    # format: abbreviated_journal year, volume, page.pdf
                    name = '{} {}, {}, {}'.format(abbreviated_journal, year, volume, page)
                    print("New name is: "+name)
                    indicator=name.split(',')[2]   
                except:
                    print('Error on find target in serializated data!')
            else:
                name='null'
        

    #处理重复的可能性
        
        print('indicator:'+indicator)  
        if (not name=='null') and (indicator not in pdfname):
            try:
                newname=(pdffolder+'\\'+name+'-'+pdfname)
                print(newname)
                os.rename(pdf, newname)
            except:
                print('Error on FileIO!')
        else:
            print('This document have been named or failed!')
    except:
        print('Error Get!')

if __name__ == '__main__':
    #try:
    print("arbv:"+sys.argv[1])
    rename(sys.argv[1] )
   # except:
    #    print('Error Get!')