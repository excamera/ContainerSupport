import zipfile
import sys
import os
import time
import random
import re
from subprocess import call
from time import sleep
import argparse

# Parser for Command line arguments
def parseCmdLineArgs():
        parser = argparse.ArgumentParser(description='Invoke Docker container')
        parser.add_argument('--image', metavar='Image',
                default='ubuntu', help='OS ImageAWS Region (Eg: ubuntu)')
        parser.add_argument('--zip', metavar='Path to ZipFile',
                help='Path to Zip of the executable to be run in container')
        parser.add_argument('--cmd', metavar='Command',
                help='The command to be run')
	parser.add_argument('--name', metavar='Name Of ZipFile', 
		help='Name of the zip file without .zip')
        parser.add_argument('--deps <items>', metavar='Dependencies',
                help='A list of dependencies, separated by commas (Q,async,:phantomjs)')
	parser.add_argument('--maintainer', metavar='Maintainer',
		default='Rahul Bhalerao', help='User/Maintainer')
        args = parser.parse_args()
        return args

# Unzip files
def unzip(zipFile, name):
	print zipFile
	if zipFile:
		zip_ref = zipfile.ZipFile(zipFile, 'r')
		zip_ref.extractall(os.getcwd())
		zip_ref.close()

# A routine to create docker file based on args
def createDockerFike(args):
	arr = []
	image = args.image
	zipFile = args.zip
	cmd = args.cmd
	maintainer = args.maintainer
	name = args.name

	arr.append("FROM " + image)
	arr.append("MAINTAINER " + maintainer)
	arr.append("RUN apt-get update")
	arr.append("RUN apt-get install -y curl git man unzip vim wget python software-properties-common python-software-properties")
	arr.append("RUN apt-get install -y python-dev python-distribute python-pip")
	arr.append("RUN DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade")
	arr.append("RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python-software-properties")
	arr.append("RUN DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common")
	arr.append("RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:mc3man/trusty-media")
	arr.append("RUN apt-get update")
	arr.append("RUN DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg gstreamer0.10-ffmpeg")
	arr.append("RUN pip install awscli boto3")
	arr.append("RUN rm -rf /var/lib/apt/lists/*")
	
	unzip(zipFile, name)
	dir = os.getcwd() + "/" + name

	arr.append("ADD " + "./" + name + " /" + name)
	arr.append("CMD chmod -R 777 /" + name)
	arr.append("CMD ls")

	fileName = getFileName()
	fw = open(fileName, "w")
	for i in arr:
		fw.write(i +"\n")
	fw.flush()
	fw.close()
	return fileName

def getFileName():
	return "videoDockerFile" + "_" + str(int(time.time())) + "_" + str(random.randint(1, 1000))
	
def spawnContainer(containerName, fileName, name, cmd):
	print("\n")
	runCmd("docker build -t " + containerName + " -f " + fileName + " .")
	print("\n")
	runCmd("docker run -itd -P -w " + "/" + name + " --name " + containerName + " " + containerName + " " + cmd)

def waitContainer(containerName):
	print("\n\n")
	run = True
	while run:
	    run = runCmd("docker inspect -f {{.State.Running}} " + containerName)
	    print("Container : " + containerName + " still running processes. Waiting to complete...")
	    sleep(2)

def checklogs(containerName, fileName):
	print("\n\n Logs:")
	runCmd("docker logs --tail=100 " + containerName);

def rmContainer(containerName):
	print("\n\n")
	runCmd("docker stop " + containerName);
	runCmd("docker rm " + containerName);

def runCmd(cmd):
	print cmd
	return os.system(cmd)

def apiCreateContainer(args):
	zip = args.zip
	name = args.name
	input_json = args.input_json
	image = args.image
	cmd = args.cmd
	fileName = createDockerFike(args)
        containerName = name.lower()
        cit_start = time.time()
        spawnContainer(containerName, fileName, name, cmd)
        cit_end = time.time()
        waitContainer(containerName)
        run_end = time.time()
        checklogs(containerName, fileName)
        rmContainer(containerName)
        print "Container Initialization time : " + str(cit_end-cit_start)
        print "Running lambda took : " + str(run_end-cit_end)

# An interface to be called by Pipeline
def createContainer():
	args = parseCmdLineArgs()
	apiCreateContainer(args)

if __name__ == "__main__":
	createContainer()
