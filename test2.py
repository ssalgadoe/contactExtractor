import codecs
import requests
import bs4
import os
import re
import urllib
import sys
from bs4 import Comment
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def keyWordsEnd(lines,keyWords,start, counter):
    for i in range (start,start+counter):
        for key in keyWords:
            #print('line->',lines[i])
            if key.lower() in lines[i].lower():
                #print('xx>', i,lines[i])
                return False;
    return True;

def isKeyInLine(keyWords,line):
    for key in keyWords:
         if key.lower().strip() in line.lower():
             return True,key;
    return False,'0';

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text    

def myParser(text,keyWords, startText, endText, countryFile):
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #text = '\n'.join(chunk for chunk in chunks)
    print(text)
    lines=text.splitlines()
    firstKeyFound = False
    lastKeyStatus = False
    lineValidated = False
    nextLineValidated = False
    lineLength= len(lines)
    print('lines->', lineLength)
    startNotFound = True
    print("startText->",startText)
    print("startText(strip)->",startText.strip())
    for index in range(0,lineLength-1):
    	curLine=lines[index]
    	if endText.strip() in curLine:
    		countryFile.write(curLine)
        	countryFile.write('\n')
        	print("found endText @", index)
        	break
    	if startNotFound:
    		if startText.strip() in curLine:
    			startNotFound=False
    			print("found startText @", index)
    		continue
    	else:
    		#tempStr = '('+ `index`+') ' + `lines[index]`
    		tempStr = lines[index]
    		#countryFile.write(tempStr)
        	#countryFile.write('\n')
    		#print(tempStr)
        	lineValidated = False
        	keyFound,key =  isKeyInLine(keyWords,lines[index])
        	if keyFound: #key found in the line
        	    print('key found', index, lines[index],key)
        	    lineValidated=False
        	    if firstKeyFound == False:#this is to find the beginning of critical area
        	        firstKeyFound = True
        	        print(index,'first key found')
        	        tempStr = lines[index-1]
        	        print(tempStr)
        	        countryFile.write(tempStr)
        	        countryFile.write('\n')
        	    print(index, lines[index])
        	    tempStr = lines[index]
        	    countryFile.write(tempStr)
        	    countryFile.write('\n')
        	    lineValidated=True
        	if firstKeyFound==True and lastKeyStatus==False and lineValidated==False:
        	    tempStr = lines[index]
        	    print(tempStr)
        	    countryFile.write(tempStr)
        	    countryFile.write('\n')
        	if keyFound:
        	    try:    
        	        lastKeyStatus= keyWordsEnd(lines,keyWords,index+1,8) #check whether still in keys display area
        	    except:
        	        print ("end of the file found")
        	        countryFile.write("----------------")
        	        countryFile.write('\n')
        	        break
        	    if lastKeyStatus:
        	        tempStr = lines[index+1]
        	        print(tempStr)
        	        countryFile.write(tempStr)
        	        countryFile.write('\n')
        	        print(index,'this is the end')
        	        #break
	              
    return;


#read urllist from a file
tempStr=""
countryData = open("test2.cfg", "r")
folderData = countryData.readline()
folderList = folderData.split('=')
folderName = folderList[1]
print(folderName)
folderDescData = countryData.readline()
folderDescList = folderDescData.split('=')
folderDesc = folderDescList[1]
print(folderDesc)

keywordsData = countryData.readline()
keywordsList = keywordsData.split('=')
keywords = keywordsList[1].split(',')
keywords = [item.lower() for item in keywords]
print(keywords)

country = folderName.strip()+".txt"
countryFile = codecs.open(country,'wb','utf-8')
countryFile.write(folderDesc)
countryFile.write('\n')

startTextData = countryData.readline()
startTextList = startTextData.split('=')
startText=startTextList[1]
print("startText",startText)

endTextData = countryData.readline()
endTextList = endTextData.split('=')
endText=endTextList[1]
print("endText",endText)

reload(sys)
#print(sys.getdefaultencoding())
sys.setdefaultencoding('utf8')

text=convert_pdf_to_txt("malaysia.pdf")
countryFile.write(text)
#myParser(text,keywords, startText, endText, countryFile)    

                       
countryData.close()
countryFile.close()





