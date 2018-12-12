import requests
import bs4
import os
import re
from bs4 import Comment

#read urllist from a file
urlData = open("list.txt", "r")
for line in urlData:
    urlList=line.split('$#$')
    print(urlList)
    #extract keywords for searching
    keyWords= urlList[1].split(',')
    print(keyWords)
    #fetch web page
    response = requests.get(urlList[0])
    soup = bs4.BeautifulSoup(response.text, "html5lib")
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
    #print(text)
    lines=text.split('\n')
    for li in lines:
        for name in keyWords:
            if name.lower() in li.lower():
                print(li)






