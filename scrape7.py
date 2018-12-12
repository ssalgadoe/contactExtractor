import codecs
import requests
import bs4
import os
import re
from bs4 import Comment



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
    countryFile.write('---------------------------------------------------------')
    print('---------------------------------------------------------')
    #fetch web page
    #print(urlList[0])
    response = requests.get(urlList[0], headers={'User-Agent': 'Mozilla/5.0'})
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

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #text = '\n'.join(chunk for chunk in chunks)
    print(text)
    lines=text.splitlines()
    index=0
    print('i am here')
    for li in lines:
        index=index+1
        for name in keyWords:
            if name.lower() in li.lower():
                if len(name.strip())+3 > len(li.strip()): #check only keyword is in the row
                    if name.lower()==keyWords[0].lower(): #first key(attribute)
                        print('\n-------')
                        countryFile.write('\n')
                        countryFile.write('\n----------------\n')
                    if not lines[index].lower() in keyWords: # key has a value
                        tempStr = li + '  ' + lines[index]
                        print(tempStr)
                        countryFile.write(tempStr)
                        countryFile.write('\n')
                    else: #key has no value <empty>
                        tempStr = li+' '
                        countryFile.write(tempStr)
                        countryFile.write('\n')
                else: #keywords and value are in same line
                    if name.lower()==keyWords[0].lower(): #first attribute
                        print('\n-------')
                        countryFile.write('\n')
                        countryFile.write('\n----------------\n')
                    tempStr = li
                    tempStr = name + '   ' + tempStr[len(name)+2:]
                    print(tempStr)
                    countryFile.write(tempStr)
                    countryFile.write('\n')
                        
urlData.close()
countryFile.close()





