import codecs
import requests
import bs4
import os
import re
from bs4 import Comment

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
    
def myParser(text,keyWords, countryFile):
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
    for index in range(0,lineLength-1):
        lineValidated = False
        keyFound,key =  isKeyInLine(keyWords,lines[index])
        if keyFound: #key found in the line
            #print(index, lines[index])
            lineValidated=True
            if firstKeyFound == False:#this is to find the beginning of critical area
                firstKeyFound = True
                print(index,'first key found')
                tempStr = lines[index-1]
                print(tempStr)
                countryFile.write(tempStr)
                countryFile.write('\n')
            try:    
                lastKeyStatus= keyWordsEnd(lines,keyWords,index+1,8) #check whether still in keys display area
            except:
                print ("end of the file found")
                countryFile.write("----------------")
                countryFile.write('\n')
                break
            if lastKeyStatus:
                print(index,'this is the end')        
        if firstKeyFound==True and lastKeyStatus==False:
                tempStr = lines[index]
                print(tempStr)
                countryFile.write(tempStr)
                countryFile.write('\n')
                      
    return;


#read urllist from a file
tempStr=""
countryData = open("atest.cfg", "r")
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
countryFile = codecs.open(country,'w','utf-8')
countryFile.write(folderDesc)
countryFile.write('\n')

notUsed = countryData.readline()
for urlData in countryData:
    url=urlData.split('<!!3!!>')
    print('load url->',url[1])
    response = requests.get(url[1], headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(response.text, "html5lib")
    #soup = bs4.BeautifulSoup(response.text)
    #remove head
    soup.head.clear()
    # kill all script and style elements
    for tag in soup():
        for attribute in ["class", "id", "name", "style"]:
            del tag[attribute]

    # get text
    text = soup.get_text()
    countryFile.write('-------------------------------------\n')
    countryFile.write(url[0])
    countryFile.write('\n-------------------------------------\n')
    myParser(text,keywords, countryFile)    

                       
countryData.close()
countryFile.close()





