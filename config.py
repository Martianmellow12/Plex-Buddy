# Config - A library for accessing the config file
#
# Written by Michael Kersting Jr.
import os
import json

location = os.path.dirname(os.path.realpath(__file__))+"\\"

#
#
# Load - Returns the contents of the config file as JSON
def load(path=location+"config.json"):
    filein = open(path, "r")
    data = filein.read()
    filein.close()
    return json.loads(data)

#
#
# Save - Saves a dictionary to the config file
def save(contents, path=location+"config.json"):
    contents = json.dumps(contents)
    fileout = open(path, "w")
    fileout.write(contents)
    fileout.close()

#
#
# Get - Returns a field from the config file
def get(field):
    return load()[field]

#
#
# List Fields - Returns the fields of the config file
def list_fields():
    return load().keys()

#
#
# Set - Sets the contents of a config file field
def set(field, data):
    config_data = load()
    config_data[field] = data
    save(config_data)
