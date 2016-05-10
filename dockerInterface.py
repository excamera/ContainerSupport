import zipfile
import sys
import os
import time
import random
import re
from subprocess import call
import argparse

# Parser for Command line arguments
def parseCmdLineArgs():
        parser = argparse.ArgumentParser(description='Invoke Docker container')
        parser.add_argument('--image', metavar='Image',
                default='ubuntu', help='OS ImageAWS Region (Eg: ubuntu)')
        parser.add_argument('--pathOfZipFile', metavar='Path to ZipFile',
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
		dir = os.getcwd() + "/" + name
		zip_ref = zipfile.ZipFile(zipFile, 'r')
		if os.path.exists(dir) == False:
			os.mkdir(dir)
		zip_ref.extractall(dir)
		zip_ref.close()

# A routine to create docker file based on args
def createDockerFike(args):
	arr = []
	image = args.image
	zipFile = args.pathOfZipFile
	cmd = args.cmd
	maintainer = args.maintainer
	name = args.name

	arr.append("FROM " + image)
	arr.append("MAINTAINER " + maintainer)
	arr.append("RUN " + "\\")
	arr.append("	apt-get update && " + "\\")
	arr.append("	apt-get install -y curl git man unzip vim wget python && " +  "\\")
	arr.append("	rm -rf /var/lib/apt/lists/*")
	unzip(zipFile, name)
	dir = os.getcwd() + "/" + name
	arr.append("ADD " + "./" + name + " /" + name)
	arr.append("RUN chmod -R 777 //" + name)
	arr.append("RUN cd /" + name + " && pwd")

	fileName = "videoDockerFile" + "_" + str(int(time.time())) + "_" + str(random.randint(1, 1000))
	fw = open(fileName, "w")
	for i in arr:
		fw.write(i +"\n")
	fw.flush()
	fw.close()
	return fileName

def spawnContainer(containerName, fileName, name, cmd):
	call(["docker-machine", "create", "--driver", "virtualbox", "video"])
	os.system("eval docker-machine env video")
	os.system("docker build -t " + containerName + " -f " + fileName + " .")
	run_cmd = "docker run -itd -P -w " + "/" + name + " --name " + containerName + " " + containerName + " " + cmd
	print run_cmd
	os.system(run_cmd)

def checklogs(containerName, fileName):
	os.system("docker logs " + containerName);
	os.system("docker logs --tail=100 " + containerName + " >" + fileName + ".log")

def rmContainer(containerName):
	os.system("docker stop " + containerName);
	os.system("docker rm " + containerName);

# An interface to be called by Pipeline
def createContainer():
	containerName="video"
	args = parseCmdLineArgs()
	fileName = createDockerFike(args)
	spawnContainer(containerName, fileName, args.name, args.cmd)
	checklogs(containerName, fileName)
	rmContainer(containerName)

if __name__ == "__main__":
	createContainer()
