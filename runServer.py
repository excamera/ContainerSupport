import server

json_string = '{ "lambda_name" : "grayscaleLambda", "cmd" : "python ./grayscaleLambda.py video.mp4 video.mp4" }'
server.setup("./grayscaleLambda.zip", json_string)
