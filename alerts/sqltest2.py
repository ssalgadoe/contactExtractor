import sys
import codecs
import requests
import bs4
import os
import re
import urllib
from bs4 import Comment
import feedparser
import time
import pymysql.cursors
from subprocess import check_output



def keyWordsEnd(lines,keyWords,start, counter):
    for i in range (start,start+counter):
        for key in keyWords:
            if key.lower() in lines[i].lower():
                return False;
    return True;

def isKeyInLine(keyWords,line):
    for key in keyWords:
         if key.lower().strip() in line.lower():
             return True,key;
    return False,'0';

   
def myParser(title,link,description,published,published2, keyWords, outputFile,connection):
    firstKeyFound = False
    lastKeyStatus = False
    lineValidated = False
    nextLineValidated = False
    keyFound,key =  isKeyInLine(keyWords,description)
    if keyFound: #key found in the line
        print('key found', title,key)
        tempStr = title + ' (' + published + ')'
        outputFile.write(tempStr)
        outputFile.write('\n')
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `alerts` (`name`, `link`,`description`,`keywords`,`published`,`published2`,`rank`) VALUES (%s,%s, %s,%s,%s,%s,%s)"
                cursor.execute(sql,(title, link, description, key,published,published2,'5'))
                connection.commit()
        except:
            print("Problem writing to the database")
    return;



configFile="rssconfig.cfg"
configFile = configFile.strip()
   
print("config file->",configFile)
#read urllist from a file
tempStr=""
try:
    configData = open(configFile, "r")
except:
    print("FileNotFound: Configuration file (",configFile,") can't be found")
    exit(0);
folderData = configData.readline()
folderList = folderData.split('=')
folderName = folderList[1]
print(folderName)
folderDescData = configData.readline()
folderDescList = folderDescData.split('=')
folderDesc = folderDescList[1]
print(folderDesc)

keywordsData = configData.readline()
keywordsList = keywordsData.split('=')
keywords = keywordsList[1].split(',')
keywords = [item.lower() for item in keywords]
print(keywords)

output = folderName.strip()+".txt"
outputFile = codecs.open(output,'w','utf-8')
outputFile.write(folderDesc)
outputFile.write('\n')

connection = pymysql.connect(host='localhost',user='capstone_user',password='dupa',
                             db='capstone',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


notUsed = configData.readline()
#-----
try:
    with connection.cursor() as cursor:
        cursor.execute('insert into alertsold (name, link, description, rank, keywords,published,published2) select name, link, description, rank, keywords,published,published2 from alerts')
        connection.commit()
except:
    print("Problem writing to the database cccc")

try:
    with connection.cursor() as cursor:
        cursor.execute('delete from alerts')
        connection.commit()
except:
    print("Problem writing to the database cccc")
    
#-----

for urlData in configData:
    urls=urlData.split('<!!3!!>')
    try:
        urlLength=len(urls[1])
        if urlLength < 5:
            continue
    except:    
        continue
    print('urlDesc',urls[0], 'load url->',urls[1])
    url = urls[1].strip()
    print("lenth", len(url))
    outputFile.write('\n-------------------------------------\n')
    outputFile.write(urls[0])
    outputFile.write('\n-------------------------------------\n')
    d = feedparser.parse(url)
    count = 1
    for post in d.entries:
        #print ('(',count,')',post.title)
        #print(post.published)
        #print('-------------------------------')
        #outputFile.write(post.title)
        #outputFile.write('\n-------------------------------------\n')
        count += 1
        myParser(post.title,post.link,post.description,post.published,post.published_parsed,keywords, outputFile,connection)    

                       
configData.close()
outputFile.close()





