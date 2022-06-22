#!/usr/bin/env python
# coding: utf-8

# In[1]:


#conda install -c conda-forge newspaper3k


# In[2]:


dataSaveLocation = 'Data'


# In[3]:


import newspaper
import json
import datetime
import os


# In[4]:


def createFolder(location):
    folder = dataSaveLocation+'/'+location
    isExist = os.path.exists(folder)

    if not isExist:
      # Create a new directory because it does not exist 
      os.makedirs(folder)
      print("The new directory is created!")


# In[76]:


def generateFilename(title, lenght):
    invalidCharacters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    title = ''.join([c for c in title if c not in invalidCharacters])
    
    
    return title[:lenght]


# In[6]:


def saveDataToJson(filename, title, author, date, text):
    
    j_data = {"Title": title, "Author": author, "Date": date, "Text": text}
    
    saveLoc = dataSaveLocation+'/'+filename+'.json'
    
    #print(saveLoc)
    with open(saveLoc, 'w') as outfile:
        json.dump(j_data, outfile,indent=4)


# In[68]:


def filterNewsURL(brand, url, date):
    TodayDate = date
    
    if (brand == 'cnn'):
        return (('cnn.com' in url) and (TodayDate.strftime("%Y/%m/%d") in url) and ('arabic' not in url) and ('cnnespanol' not in url) and ('videos' not in url))
    elif (brand == 'cnbc'):
        return (('cnbc.com' in url) and (TodayDate.strftime("%Y/%m/%d") in url) and ('/video/' not in url))
    elif (brand=='npr'):
        return (('npr.org' in url) and (TodayDate.strftime("%Y/%m/%d") in url))
    elif (brand=='businessinsider'):
        return ('www.businessinsider.com' in url)
    elif (brand=='insider'):
        return ('www.insider.com' in url)
    elif (brand=='nytimes'):
        return ((TodayDate.strftime("%Y/%m/%d") in url) and ('www.nytimes.com' in url) and ('/video/' not in url) and ('/interactive/' not in url))
    elif (brand=='nbcnews'):
        return (('nbcnews.com' in url) and ('/video/' not in url))
    elif (brand=='politico'):
        return (TodayDate.strftime("%Y/%m/%d") in url)
    elif (brand=='nypost'):
        return ('nypost.com' in url) and (TodayDate.strftime("%Y/%m/%d") in url) and ('/video/' not in url)
    elif (brand=='latimes'):
        return (('latimes.com' in url) and (TodayDate.strftime("%Y-%m-%d") in url) and ('/espanol/' not in url))
    


# In[87]:


def scrapePaper(url):
    paper = newspaper.build(url, language='en', memoize_articles=False)
    print(paper.brand)
    TodayDate = datetime.datetime.now()

    #filter Articles
    filteredArticles = []
    for article in paper.articles:
        url = article.url
        if filterNewsURL(paper.brand, url, TodayDate):

            #print(article.url)
            filteredArticles.append(article)
    print(str(len(filteredArticles)) + ' out of '+str(len(paper.articles)))
    
    
    #Create Directory
    directory = paper.brand+'/'+TodayDate.strftime("%Y-%m-%d")
    createFolder(directory)
    
    print('Start Scrape')
    #Scrape Articles
    
    count = 0
    for article in filteredArticles:
        #print(article.publish_date)
        #article = filteredArticles[0]
        try:
            article.download()
            article.parse()

            title = article.title

            author = article.authors
            #author = ', '.join(author)

            date = article.publish_date
            date = date.strftime("%m-%d-%Y")

            text = article.text

            filename = generateFilename(title, 40)
            #print(title)

            #Filter by date of article
            #print(date)
            if (date == TodayDate.strftime('%m-%d-%Y')):
                #print(title)
                count = count + 1
                saveDataToJson(directory+'/'+filename, title, author, date, text)

        except:
            pass
    print('Number of Articles Saved: '+str(count))
    print('-------------------------')


# In[94]:


sources = ['http://cnn.com', 'http://www.cnbc.com', 'http://www.npr.org', 'http://www.insider.com',
           'http://www.businessinsider.com', 'http://nytimes.com', 'http://www.nbcnews.com', 
           'http://www.politico.com', 'http://www.nypost.com', 'http://www.latimes.com']
len(sources)


# In[ ]:


for source in sources:
    print(source)
    scrapePaper(source)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


'''


# In[91]:


#url = sources[7]
url = 'http://www.insider.com'
paper = newspaper.build(url, language='en', memoize_articles=False)
paper.brand


# In[92]:


for article in paper.articles:
    print(article.url)
print(len(paper.articles))


# In[56]:


TodayDate = datetime.datetime.now()

#filter Articles
filteredArticles = []
for article in paper.articles:
    url = article.url
    #if (TodayDate.strftime("%Y/%m/%d") in url) and ('/video/' not in url):
    if ('www.insider.com' in url):

        print(url)
        filteredArticles.append(article)
print(str(len(filteredArticles)) + ' out of '+str(len(paper.articles)))

#return filteredArticles


# In[44]:


TodayDate = datetime.datetime.now()

#filter Articles
filteredArticles = []
for article in paper.articles:
    url = article.url
    #if (TodayDate.strftime("%Y/%m/%d") in url) and ('video' not in url):
    if filterNewsURL(paper.brand, url, TodayDate):

        print(url)
        filteredArticles.append(article)
print(str(len(filteredArticles)) + ' out of '+str(len(paper.articles)))

#return filteredArticles


# In[ ]:


for article in filteredArticles:
    print(article.url)
    #article = filteredArticles[0]
    try:
        article.download()
        article.parse()

        title = article.title

        author = article.authors
        #author = ', '.join(author)

        date = article.publish_date
        date = date.strftime("%m-%d-%Y")

        print(title)
        if (date == TodayDate.strftime('%m-%d-%Y')):
            print(date)

    except:
        pass


# In[55]:



#for article in filteredArticles:
article = filteredArticles[3]
article.download()
article.parse()
print('URL: ', article.url)
print('TITLE: ', article.title)

print('AUTHORS: ', article.authors)
        #author = ', '.join(author)

print('PUBLISH DATE: ',article.publish_date)
#date = date.strftime("%m-%d-%Y")

print(article.text)


# In[ ]:





# In[ ]:


http://cnn.com
#http://www.huffingtonpost.com
#http://www.time.com
http://www.cnbc.com
get_ipython().run_line_magic('pinfo2', 'http')
http://www.npr.org
http://www.businessinsider.com
#http://www.theinsider.com
http://nytimes.com
http://www.nbcnews.com
get_ipython().run_line_magic('pinfo2', 'http')
http://www.politico.com
http://www.nypost.com
http://www.latimes.com
#http://www.forbes.com


# In[ ]:





# In[ ]:


newspaper.popular_urls()


# In[ ]:


'''

