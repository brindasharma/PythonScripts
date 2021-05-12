#!/usr/bin/env python
# coding: utf-8

# In[15]:
#Use the Client ID and Client Secret to create a post request to ArcGIS REST endpoint "/token"  and generate an access token at app level
#This is an alternate if user has a SSO login and cannot generate token using username and password, but licensing terms might be violated in certain use cases so consult the Esri team. This is more for prorotyping or for internal use
import requests

def generate_token(c_id, secret):
    payload = {
        'client_id': c_id,
        'client_secret': secret,
        'grant_type': 'client_credentials',
        'expiration': 1440
    }
    
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'f': 'json'
    }
    request = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token', headers=headers, data=payload, params=params)
    response = request.json()
    token = response['access_token']
    return token
    


# In[18]:
#Call the generate token function here by passing the application Client Id and Client Secret. This application is created as an item in your ArcGIS Online account

token=generate_token(c_id=".............",secret="...................")



# In[26]:
#Create a request to a user feature service using the access token obtained in previous step

request = requests.post('https://services.arcgis.com/q7zPNeKmTWeh7Aor/arcgis/rest/services/Sample/FeatureServer?token=NwU7iZR47ZhTpyJcF8xmAnZrwjpNEAEvUxDqatPAi2jp4EdlhSPBYDJ5cP941aRqAdYtbhurp_FVNWYn2Z783OsV95t0Re4oBs_hkqzbWpJ00ym9Zccc1q27Ho3Xf_WEztEUus69vpcH9Cd31zRQkA..&f=json')
request.json()


# In[ ]:

#create a query request using the above token:
#https://services1.arcgis.com/dis-mine/arcgis/rest/services/my-name/FeatureServer/0/query?where=blahblah*outfields=*&token=YOURTOKEN&f=json



