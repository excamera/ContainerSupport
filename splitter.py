import time
import os
import sys

def getSplitDir(job_name):
     return job_name + "/inputsplit"

def split(job_name, video):
     os.mkdir(getSplitDir(job_name))
