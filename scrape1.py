import requests
import bs4
import os
import re
from bs4 import Comment
response = requests.get('https://www.routcom.com/support.html')
soup = bs4.BeautifulSoup(response.text, "html5lib")

#remove head
soup.head.clear()

#remove anchors
for a in soup.findAll('a'):
    a.extract()

#remove comments    
comments = soup.findAll(text=lambda text:isinstance(text, Comment))
for comment in comments:
    comment.extract()

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
print(text)




