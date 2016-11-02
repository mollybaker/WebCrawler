
import sys
import requests
from time import sleep
from bs4 import BeautifulSoup
import settings

url = raw_input("Please enter a website in the format of www.example.com: ")
keyword = raw_input("Please enter the keyword you would like to search for: ")

#Check the input for correct formatting
correctFormat = False
while correctFormat == False:
    try:
        formattedUrl  = requests.get("http://" +url)
        correctFormat = True
    except requests.exceptions.ConnectionError: 
        correctFormat = False
        print "Error: Input of website is improperly formatted. Be sure to use a website in the format of 'www.example.com'"
        url = raw_input("Please enter a website in the format of www.example.com: ")
        keyword = raw_input("Please enter the keyword you would like to search for: ")
        
#Uses BeautifulSoup to search through the text on the page
pageData = formattedUrl.text
soup = BeautifulSoup(pageData, "lxml")

# ********  Search for the keyword
print "Searching..."
#Checks main site first
if keyword in soup.get_text():
    print "Keyword: %s was found at %s " % (keyword, url)

#For other pages on the site:
for link in soup.find_all('a'):
    nextUrl = link.get('href')
    if nextUrl.startswith('http') == False:
        formattedLink = url + nextUrl
        nextRequest = requests.get("http://" + formattedLink)
        nextPage = nextRequest.text
        soup = BeautifulSoup(nextPage, "lxml")
        if keyword in soup.get_text():
            print "Keyword: %s was found at %s " % (keyword, formattedLink)
    else:
        newRequest = requests.get(nextUrl)
        nextPage = nextRequest.text
        soup = BeautifulSoup(nextPage, "lxml")
        if keyword in soup.get_text():
            print "Keyword: %s was found at %s: " % (keyword, nextUrl)
    #Sleep for two seconds needed to prevent blacklisting IP
    sleep(2)  

# ********
