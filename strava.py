#!/usr/bin/python

from __future__ import print_function

import sys
import datetime
import json
import os, stat
from subprocess import call as call

# Original stravaup.py imports
from stravalib import Client, exc
from sys import stderr, stdin
from tempfile import NamedTemporaryFile
import os.path, gzip
import configparser as ConfigParser
import argparse
from io import StringIO
import requests
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from gi.repository import GObject as gobject

class Strava:

   def read_strava_tokens(self):
       # Read the token from the saved file
       with open('strava_tokens.json', 'r') as tokens:
           data = json.load(tokens)

       return data


   def get_access_token(self):
       print("get_access_token()")
       data = self.read_strava_tokens()

       # Get the access token
       access_token = data['access_token']
       return access_token


   def get_refresh_token(self):
       print("get_refresh_token()")

       data = read_strava_tokens()

       # Get the refresh token
       refresh_token = data['refresh_token']
       return refresh_token

   def refresh_access_token(self):
       print("refresh_access_token")

       data = self.read_strava_tokens()
       print("data = ", data)

       accessToken = data['access_token']
       refreshToken = data['refresh_token']

       cid = xxxxxx # CLIENT_ID from stravacli
       client_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

       client = Client(accessToken)
       tokens = client.refresh_access_token(cid, client_secret, refreshToken)

       newAccessToken = tokens['access_token']
       newRefreshToken = tokens['refresh_token']
       newExpiresAt = tokens['expires_at']

       print ("new access token=", newAccessToken, " new refresh token=", newRefreshToken, " new expires at=", newExpiresAt)

       data['access_token'] = newAccessToken
       data['refresh_token'] = newRefreshToken
       data['expires_at'] = newExpiresAt

       print("new data=", data)

       #Save json response as a variable

       with open('strava_tokens.json', 'w') as outfile:
          json.dump(data, outfile)


   def upload_activities(self, activities):
       if len(activities) == 0:
           print("No new activities")
           return True

       accessToken = self.get_access_token()

       client = Client(accessToken)
       try:
           athlete = client.get_athlete()
       except requests.exceptions.ConnectionError:
           print("Could not connect to Strava API")
           return False
       except Exception as e:
           print("Not authorized at Strava")
           return False

       print("Welcome {} {} (id {:d}).".format(athlete.firstname,
                                            athlete.lastname, athlete.id))
       for f in activities:
           base, ext = os.path.splitext(f)
           cf =  NamedTemporaryFile(suffix='.gz')
           gzip.GzipFile(fileobj=cf, mode='w+b').writelines(open(f, "rb"))
           print("Uploading activity from {}...".format(f))

           title = "Exercise Bike"
           desc = "PiBike upload"

           # Upload compressed activity
           try:
               cf.seek(0, 0)
               upstat = client.upload_activity(cf, ext[1:] + '.gz',
                                               title,
                                               desc,
                                               activity_type='ride',
                                               private=False)
                                               # TODO detect activity_type somehow?
               activity = upstat.wait()
               duplicate = False
           except exc.ActivityUploadFailed as e:
               words = e.args[0].split()
               if words[-4:-1]==['duplicate','of','activity']:
                   activity = client.get_activity(words[-1])
                   #print(f + ": duplicate")
                   duplicate = True
               else:
                   print(f + ": " + e.args[0])
                   return False

           # Show results as URL and open in browser
           uri = "http://strava.com/activities/{:d}".format(activity.id)
           print("{}{}".format(uri, " (duplicate)" if duplicate else ''))
           #webbrowser.open_new_tab(uri)
       return True


   def uploadGPXfile(self, filename):

      print("Started: " + datetime.datetime.today().strftime("%s") )

      self.refresh_access_token()
      upload_list = []

      upload_list.append(filename)
      #print ("List of GPX to upload: ", upload_list)
 
      # Upload new GPX files
      result = self.upload_activities(upload_list)

      return result


