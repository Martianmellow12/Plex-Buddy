# Make Config - Creates a config file for Plex Buddy
#
# Written by Michael Kersting Jr.
import os
import sys
import json
import getpass
import plex
from slackclient import SlackClient

# Get the scripts location
location = os.path.dirname(os.path.realpath(__file__)) + "\\"
print "Using %s as working directory" % location

# Check for an older config file
if os.path.isfile(location+"config.json"):
    print "Config file already exists. Overwrite it?"
    while True:
        response = raw_input("(y/n) ").lower()
        if response == "y": break
        elif response == "n": sys.exit(0)
        else: print "Please enter either \"y\" or \"n\" without quotes"

#
#
# Gather the information needed to create the config file
print ""
print "Creating config file now"

# Get the token
slack_token = raw_input("Slack Legacy Token > ")
print "Testing the token...",
client = SlackClient(slack_token)
response = client.api_call("api.test")
if response["ok"] == True:
    print "OK"
else:
    print "FAILED"
    print "Error: %s" % response["error"]
    sys.exit(0)
print ""

# Get the monitor directories
print "Plex buddy can monitor directories and send notifications when files are added or removed. Enter the directories you would like to have monitored below, separated by pipes (|)"
monitor_directories = raw_input("> ").split("|")
while "" in monitor_directories:
    monitor_directories.remove("")
errors = list()
for i in monitor_directories:
    print "Checking \"%s\"..." % i,
    if not os.path.isdir(i):
        print "FAILED"
        errors.append(i)
    else:
        print "OK"
if len(errors) > 0:
    for i in errors:
        monitor_directories.remove(i)
    print "One or more directories failed checks, and were removed"
print ""

#
#
# Get the Plex token
print "To interface with your Plex server, you must log in. Your email and password will NOT be stored."
print "Enter your Plex login credentials"
plex_email = raw_input("Email > ")
plex_password = getpass.getpass("Password > ")
print "Getting Plex auth token...",
try:
    plex_token = plex.get_token(plex_email, plex_password)
except Exception, e:
    print "FAILED"
    print "Exception: " + str(e)
    sys.exit(0)
print "OK"
print ""

#
#
# Write the config information to a file
print "Creating JSON object to write to file...",
try:
    data = {
        "slack_token":slack_token,
        "plex_token":plex_token,
        "monitor_dirs":monitor_directories
        }
    data_json = json.dumps(data)
except Exception, e:
    print "FAILED"
    print "Exception: %s" % str(e)
    sys.exit(0)
print "OK"

print "Writing config information to file...",
try:
    fileout = open(location+"config.json", "w")
    fileout.write(data_json)
    fileout.close()
except Exception, e:
    print "FAILED"
    print "Exception: %s" % str(e)
    sys.exit(0)
print "OK"

# Finish up
print "Config file created successfully"
sys.exit(0)
