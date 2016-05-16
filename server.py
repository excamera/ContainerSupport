import os
import sys
import time
import json
import dockerInterface

class environment:
    zip = ""
    name = ""
    image = ""
    input_json = ""
    maintainer = ""
    cmd = ""
   
    def __init__(self, zip, name, input_json, image, cmd):
	self.zip = zip
	self.name = name
	self.image = image
	self.input_json = input_json
	self.maintainer = os.popen('whoami').read()
	self.cmd = cmd

def setup(zipFile, input_json):
    if "/" in zipFile:
	print("ZipFile in local filesystem")
	if os.path.exists(zipFile) == False:
	    print("ZipFile not found. Exiting...")
	    sys.exit()
	invokeContainer(zipFile, input_json)
    else:
	print("ZipFile in S3 Store")
	invokeLambda(zipFile, input_json)

def getCmd(video):
        return "python handler.py " + video

def invokeContainer(zipFile, input_json):
    print("Invoking Docker Container")
    j = json.loads(input_json)
    name = j['lambda_name']
    video = j['key']
    image = "ubuntu:14.04"
    cmd = getCmd(video)
    env = environment(zipFile, name, input_json, image, cmd)
    dockerInterface.apiCreateContainer(env)

def invokeLambda(zipFile, input_json):
    print("Invoking AWS Lambda")
