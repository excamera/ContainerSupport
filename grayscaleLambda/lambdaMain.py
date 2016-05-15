from __future__ import print_function
import os
import sys
import uuid
import logging
import time
from random import randint
import subprocess as sp

FFMPEG_BIN = "ffmpeg"

sys.path.append(".") 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
   
def grayscale_chunk(path, video_name):
    output_file_name =  video_name.split(".")[0] + "gray." + video_name.split(".")[1]
    command = [ FFMPEG_BIN,
            '-i', path,
            '-vf', 'hue=s=0',
            '-c:a', 'copy',
            '-safe', '0',
            "/tmp/" + output_file_name
            ]
    try :
       sp.check_output(command)
    except sp.CalledProcessError as e:
        logger.info("the exception is " + str(e.output) + " -------------")
    return output_file_name

def cleanup_files(video_filepath):
    sp.check_call(["rm", "-rf", video_filepath+"*"])
    
def handler(download_path, video_name):
    output_file_name = grayscale_chunk(download_path, video_name)
    cleanup_files(download_path)

if len(sys.argv) >= 1:
	path = sys.argv[1]
	if len(sys.argv) >= 2:
	    video_name = sys.argv[2]
	else:
	    print("Video name not supplied. Exiting...")
	    sys.exit()
else:
	print("Path not supplied. Exiting...")
	sys.exit()

handler(path, video_name)
