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
    for index, li in enumerate(lines):
        lineValidated = False
        for key in keyWords:
            if key.lower() in li.lower():
                lineValidated = True  # line is validated
                if firstKeyFound == False:
                    firstKeyFound = True
                    print(index,'first key found')
                    tempStr = '<' +lines[index-1] + '>'
                    print(tempStr)
                    countryFile.write(tempStr)
                    countryFile.write('\n')
                if len(key.strip())+3 > len(li.strip()): #keywords and values are in different lines
                    if key.lower()==keyWords[0].lower(): #first key(attribute)
                        print('-------')
                        countryFile.write('\n')
                    if not lines[index+1].lower() in keyWords: # key has a value
                        tempStr = li + '  ' + lines[index+1]
                        print(tempStr)
                        countryFile.write(tempStr)
                        countryFile.write('\n')
                    else: #key has no value <empty>
                        tempStr = li+' '
                        countryFile.write(tempStr)
                        countryFile.write('\n')
                else: #keywords and value are in same line
                    if key.lower()==keyWords[0].lower(): #first attribute
                        countryFile.write('\n')
                    tempStr = li
                    tempStr = key + '   ' + tempStr[len(key)+2:]
                    print(index, tempStr)
                    countryFile.write(tempStr)
                    countryFile.write('\n')
                lastKeyStatus= keyWordsEnd(lines,keyWords,index+1,5) #check whether still in keys display area
                if lastKeyStatus:
                    print(index,'this is the end')
        if firstKeyFound==True and lastKeyStatus==False and lineValidated==False:
            tempStr = '<' + li +'>'
            print(tempStr)
            countryFile.write('\n') 
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





