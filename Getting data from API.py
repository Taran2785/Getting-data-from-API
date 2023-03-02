#!/usr/bin/env python
# coding: utf-8

# # Getting Music Data with API using Python

# We’ll be working with the Last.fm API. Last.fm is a music service that builds personal profiles by connecting to music streaming apps like iTunes, Spotify and others like it and keeping track of the music you listen to.We’ll be building a dataset of popular artists using their API.
# 
# 

# In[13]:


get_ipython().system('pip install requests')


# In[14]:


import requests


# ### Authenticating with API Keys
# 

# In[15]:


# First API request

API_KEY = '532cf10ba3f4a5887b97458e53ca5d69'
USER_AGENT = 'Taranjit _Kaur'


# ### Import the requests library, create a dictionary for our headers and parameters, and make our first request!

# In[16]:


import requests

headers = {
    'user-agent': USER_AGENT
}

payload = {
    'api_key': API_KEY,
    'method': 'chart.gettopartists',
    'format': 'json'
}

r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
r.status_code


# ### Create a function

# In[17]:


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


# In[18]:


r = lastfm_get({
    'method': 'chart.gettopartists'
})

r.status_code


# ### Print our response from the API:

# In[19]:


import json

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(r.json())


# In[20]:


jprint(r.json()['artists']['@attr'])


# ### Working with Paginated Data
# 

# In[21]:


import time
from IPython.core.display import clear_output

responses = []

page = 1
total_pages = 99999 # this is just a dummy number so the loop starts

while page <= total_pages:
    payload = {
        'method': 'chart.gettopartists',
        'limit': 500,
        'page': page
    }

    # print some output so we can see the status
    print("Requesting page {}/{}".format(page, total_pages))
    # clear the output to make things neater
    clear_output(wait = True)

    # make the API call
    response = lastfm_get(payload)

    # if we get an error, print the response and halt the loop
    if response.status_code != 200:
        print(response.text)
        break

    # extract pagination info
    page = int(response.json()['artists']['@attr']['page'])
    total_pages = int(response.json()['artists']['@attr']['totalPages'])

    # append response
    responses.append(response)

    # if it's not a cached result, sleep
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)

    # increment the page number
    page += 1


# ### Processing the data

# In[23]:




import pandas as pd

r0 = responses[0]
r0_json = r0.json()
r0_artists = r0_json['artists']['artist']
r0_df = pd.DataFrame(r0_artists)
r0_df.head()


# In[24]:


frames = [pd.DataFrame(r.json()['artists']['artist']) for r in responses]
artists = pd.concat(frames)
artists.head()

