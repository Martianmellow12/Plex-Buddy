# Plex Refresh - Function that refreshes a local Plex library at 127.0.0.1:32400
#
# Written by Michael Kersting
import json
import requests

#
#
# Get Token - Gets a token to make requests with Plex
def get_token(username, password, version="1.0"):
    url = "https://plex.tv/users/sign_in.json"
    data = "user%5Blogin%5D="+username+"&user%5Bpassword%5D="+password
    headers = {
        "X-Plex-Client-Identifier":"PLEXBUDDY-SLACKBOT",
        "X-Plex-Product":"Plex Buddy (Slack Bot)",
        "X-Plex-Version":str(version)
        }
    response = requests.post(url, data=data, headers=headers).content
    response = json.loads(response)
    if "error" in response.keys(): return None
    return response["user"]["authToken"]

#
#
# Refresh Library - Refreshes Plex libraries
def refresh_library(token, ip_address="127.0.0.1"):
    url = "http://%s:32400/library/sections/all/refresh?X-Plex-Token=%s" % (ip_address, token)
    requests.get(url)
