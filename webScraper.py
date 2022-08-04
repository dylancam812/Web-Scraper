import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.cs.hmc.edu/people/"
results = requests.get(url)

soup = BeautifulSoup(results.text, "html.parser")

#initiate data storage
name = []
title = []
office = []
phone = []
email = []
website = []

profInfo_div = soup.find_all('div', class_="prof_info")

#our loop through each container
for container in profInfo_div:

    #individual and job
    if container.a.h3 == None:
        if container.h3 == None:
            individual = ''
            job = ''
        else:
            individualAndJob = container.h3.text
            individual = individualAndJob[0:individualAndJob.index(',')]
            individual = ''.join(filter(lambda x: x.isalpha() or x.isspace(), individual)).strip()
            job = individualAndJob[individualAndJob.index(',')+2:len(individualAndJob)]
    else:
        individualAndJob = container.a.h3.text
        individual = individualAndJob[0:individualAndJob.index(',')]
        individual = ''.join(filter(lambda x: x.isalpha() or x.isspace(), individual)).strip()
        job = individualAndJob[individualAndJob.index(',')+2:len(individualAndJob)]  
    name.append(individual)
    title.append(job)

    #workplace
    if not(container.div.dl.dt == None):
        if (container.div.dl.dd != None) and (container.div.dl.dt.text == "Office:"):
            workplace = container.div.dl.dd.text
        else:
            workplace = ''
    office.append(workplace)

    #cellphone
    cellphone = '' 
    for x in container.div.dl:
        for y in x:
            if y == None:
                cellphone = ''
            elif "(" in y:
                cellphone = y 
    phone.append(cellphone)

    #emailAdress
    emailAdress = '' 
    for x in container.div.dl:
        for y in x:
            for z in y:
                if z == None:
                    emailAdress = ''
                elif "@" in z:
                    emailAdress = z
    email.append(emailAdress)

    #personalWebsite
    personalWebsite = '' 
    for x in container.div.dl:
        for y in x:
            for z in y:
                if z == None:
                    personalWebsite = ''
                elif "http" in z:
                    personalWebsite = z
    website.append(personalWebsite)

#pandas dataframe        
info = pd.DataFrame({
'name': name,
'title': title,
'office': office,
'phone': phone,
'email': email,
'website': website,
})

#add dataframe to csv file named 'movies.csv'
info.to_csv('info.csv')