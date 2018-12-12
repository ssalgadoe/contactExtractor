import sys
import codecs
#import requests
import bs4
import os
import re
import urllib
from bs4 import Comment
import feedparser
import time
import pymysql.cursors
from subprocess import check_output

keywordStart="<keywords-start>"
keywordEnd="<keywords-end>"
rssFeedList="<rssFeedList>"
keywords={}
keyValue={}
urlValue={}

def isKeyInLine(keyWords,line):
    for i in range(len(keyWords)):
         if keyWords[i].strip() in line.lower():
             return True,keyWords[i],keyValue[i];
    return False,'0','0';

def isKeyInLineEx(keyWords,keyValue,line,urlRank):
    total=0
    foundKeyList=""
    keyFound=False
    for i in range(len(keyWords)):
         if keyWords[i].strip() in line.lower():
             #print("foundkey", keyWords[i],"->",keyValue[i],total)
             foundKeyList=foundKeyList+":"+keyWords[i]
             total = total+ int(keyValue[i])
             keyFound=True
    cost = total*int(urlRank)
    return keyFound,foundKeyList,cost;


def myParser(urlRank,title,link,description,published,published2, keyWords, keyValue, outputFile,connection):
    firstKeyFound = False
    lastKeyStatus = False
    lineValidated = False
    nextLineValidated = False
    enabled='on'
    keyFound,key,rank =  isKeyInLineEx(keyWords,keyValue,description,urlRank)
    if keyFound: #key found in the line
        print('key found', title,key,rank)
        tempStr = title + ' (' + published + ')'
        outputFile.write(tempStr)
        outputFile.write('\n')
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `alerts` (`name`, `link`,`description`,`keywords`,`published`,`published2`,`rank`,`enabled`) VALUES (%s,%s, %s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,(title, link, description, key,published,published2,rank,enabled))
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
keySegment=False
rssSegment=False
ucounter=0
kcounter=0
for line in configData.readlines():
    line=line.strip('\n')
    if keywordEnd in line:
        print("keyword End")
        keySegment=False
        totalKeys=kcounter
    if keywordStart in line:
        print("keyword start")
        keySegment=True
        continue
    if keySegment:
        s=line.split('=')
        keywords[kcounter]=s[0]
        keyValue[kcounter]=s[1]
        kcounter=kcounter+1
    if rssFeedList in line:
        print("rss list start")
        rssSegment=True
        continue
    if rssSegment:
        s=line.split('<!!3!!>')
        urlValue[ucounter]=s[1]
        urlValue[ucounter+1]=s[2]
        ucounter=ucounter+2
            
            
        
       
#print(keywords)
#print(urlValue)
#print(keyValue)
output = folderName.strip()+".txt"
outputFile = codecs.open(output,'w','utf-8')
outputFile.write(folderDesc)
outputFile.write('\n')

connection = pymysql.connect(host='localhost',user='root',password='',
                             db='ingle',
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
urlListSize = len(urlValue)
print("size", urlListSize)
i=0
while(i+1 < urlListSize):
    urlRank=urlValue[i]
    url=urlValue[i+1]
    print(urlRank,"-",url)
    i=i+2
    try:
        urlLength=len(url)
        if urlLength < 5:
            continue
    except:    
        continue
    print('urlRank',urlRank, 'load url->',url)
    url = url.strip()
    print("lenth", len(url))
    outputFile.write('\n-------------------------------------\n')
    outputFile.write(url)
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
        myParser(urlRank, post.title,post.link,post.description,post.published,post.published_parsed,keywords,keyValue, outputFile,connection)    

                       
configData.close()
outputFile.close()





