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
         if key.lower() in line.lower():
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
    #print(text)
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
            lastKeyStatus= keyWordsEnd(lines,keyWords,index+1,5) #check whether still in keys display area
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
urlData = open("list.txt", "r")
for line in urlData:
    urlList=line.split('<!!3!!>')
    print(urlList)
    #extract keywords for searching
    keyWords= urlList[1].split(',')
    keyWords = [item.lower() for item in keyWords]
    print(keyWords)
    country = urlList[2]
    country = country.strip()+".txt"
    print(country)
    countryFile = codecs.open(country,'w','utf-8')
    countryFile.write('---------------------------------------------------------\n')
    print('---------------------------------------------------------')
    #fetch web page
    #print(urlList[0])
    response = requests.get(urlList[0], headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(response.text, "html5lib")
    #remove head
    soup.head.clear()
    # kill all script and style elements
    for tag in soup():
        for attribute in ["class", "id", "name", "style"]:
            del tag[attribute]

    # get text
    text = soup.get_text()
    myParser(text,keyWords, countryFile)


                        
urlData.close()
countryFile.close()





