# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 20:52:25 2017
Scraping the website for exhibitors info including their emails
http://www.highpointmarket.org/exhibitor/25/0/0/0/0/0/0/all

@author: Hsemu
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import re


#Opening up the connection and grabbing the page
my_url="http://www.highpointmarket.org/exhibitor/25/0/0/0/0/0/0/all"


#Reduced link for getting to the pages inside website:
link_url="http://www.highpointmarket.org"    
    
#my_url="http://www.bunakara.com"

#Defining the function for parsing urls

def gethtmlpage(my_url):
    
    uClient=uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    
    #html Parsing
    page_soup=soup(page_html,"html.parser")
    return(page_soup);


#Parsing to html
url_split=my_url.split(".")
page_soup=gethtmlpage(my_url)

#geting the contact us from pages
for elem in page_soup.find_all('a', href=re.compile(url_split[0]+'\.'+url_split[1]+'\.com'+'/contact')):
    print(elem['href'])

#Grabs each name of exhibitor
containers=page_soup.findAll("div",{"class":"table-col table-span-12-12"})
#getting the showroomm and shuttle
containers2=page_soup.findAll("div",{"class":"table-col table-span-8-12 text"})
#Getting the exhibitor links
containers3=[]
for elem in page_soup.find_all('a', href=re.compile('/exhibitor/details')):
    containers3.append(elem['href'])

numb_exhibitors=len(containers)
numb_showrooms=len(containers2)

#Showroom
print(containers2[0].text.split("Showroom:",1)[1].split("Shuttle Stop:",1)[1])
#Shuttle
print(containers2[0].text.split("Showroom:",1)[1].split("Shuttle Stop:",1)[0])

#Getting the Link for Website

websitelinks=[link_url+x for x in containers3]

links_for_excel=[]
linkonhighpoint=[]
#websitelinks="http://www.highpointmarket.org/exhibitor/details/6467"

page_link=gethtmlpage(websitelinks)
gettingfulltext=page_link.findAll("div",{"class":"table-col table-span-8-12 text pad-left-20"})

for link in websitelinks:
    page_link=gethtmlpage(link)
    gettingfulltext=page_link.findAll("div",{"class":"table-col table-span-8-12 text pad-left-20"})
    if(gettingfulltext[0].find_all('a', href=re.compile('www'))==[]):
        links_for_excel.append('')
        linkonhighpoint.append('')
        print("value for "+link+" is "+' blank')
    else:
        for elem in gettingfulltext[0].find_all('a', href=re.compile('www')):
            links_for_excel.append(elem['href'])
            linkonhighpoint.append(link)
            print("value for "+link+" is "+elem['href'])

     

#for link in websitelinks:
#    print(link)
#    page_link=gethtmlpage(link)
#    gettingfulltext=page_link.findAll("div",{"class":"table-col table-span-8-12 text pad-left-20"})
#    for elem in gettingfulltext[0].find_all('a', href=re.compile('www')):
#        links_for_excel.append(elem['href'])
#        print("value for "+link+" is "+elem['href'])

len(links_for_excel)
## Suppose we have a text with many email addresses
str = page_soup.text
value=[]
## Here re.findall() returns a list of all the found email strings
emails = re.findall(r'[\w\.-]+@[\w\.-]+', str) 
    ## ['alice@google.com', 'bob@abc.com']    
for email in emails:
    # do something with each found email string
    value.append(email)
    print(value)



filename="Exhibitors.csv"
f=open(filename,"w")

headers="Name"+"|"+"Location"+"|"+"Transportation"+"|"+"URL"+"\n"

f.write(headers)

for i in range(0,numb_exhibitors):
         name_exhibitor=containers[i].h2.text
         name_showroom=containers2[i].text.split("Showroom:",1)[1].split("Shuttle Stop:",1)[1].strip()
         name_shuttle=containers2[i].text.split("Showroom:",1)[1].split("Shuttle Stop:",1)[0].strip()
         URL_links=links_for_excel[i].strip()
         show_profile=linkonhighpoint[i].strip()
         f.write(name_exhibitor+"|"+name_showroom+"|"+name_shuttle+"|"+URL_links+"|"+show_profile+"\n")
f.close()



    
    
