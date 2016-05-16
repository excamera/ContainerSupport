from __future__ import print_function
import boto3
import os
import sys
import uuid
import logging
import time
import json
from random import randint
import subprocess as sp

FFMPEG_BIN = "ffmpeg"
TEMP_BUCKET_NAME=""

sys.path.append(".")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

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
    
def run(download_path, video_name):
    output_file_name = grayscale_chunk(download_path, video_name)
    cleanup_files(download_path)

def handler_docker():
    if len(sys.argv) >= 1:
	download_path = sys.argv[1] 
	video_name = download_path
    output_file_name = grayscale_chunk(download_path, video_name)
    cleanup_files(download_path)
    return output_json(output_file_name)

def output_json(output_file_name):
    return {'output_key' : output_file_name}

def handler(event, context):
    bucket = TEMP_BUCKET_NAME
    key = event['key']
    video_name = '{}{}'.format(uuid.uuid4(), key)
    download_path = '/tmp/%s' % video_name
    s3_client.download_file(bucket, key, download_path)
    output_file_name = grayscale_chunk(download_path, video_name)
    cleanup_files(download_path)
    s3_client.upload_file("/tmp/" + output_file_name, bucket, output_file_name)
    return {'output_key' : output_file_name}

if __name__ == "__main__":
    handler_docker()
