import os
import sys
import time
import random
import splitter

def getJobID():
    id = str(time.time())
    return "job_" + id

def cleanup(code):
    print "Cleaning up..."
    sys.exit()

def invokeContainer(zipFile, video):
    if (!os.path.exists(zipFile)):
	print "ZipFile " + zipFile + " does not exist"
	cleanup(1)
    if (!os.path.exists(video)):
	print "Video " + video + " does not exist"
	cleanup(1)
    job_name = getJobID()
    print "Creating job " + job_name + "..."
    if (os.path.exists(job_name)):
	print "Job " + job_name + "already exists"
	cleanup(1)
    os.mkdir(job_name)
    print "All outputs related to this job can be found at : " + job_name

    print "Splitting the video " + video + "..."
    if (splitter.split(job_name, video) == True):
	print "Split is successful..."
    else:
	cleanup(1)

    print "Spawning containers..."
    spawn.spawnContainer(job_name, zipFile, video, tag)

