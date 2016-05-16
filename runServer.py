import server

json_string = '{ "lambda_name" : "grayscaleLambda", "key" : "video.mp4" }'
server.setup("./grayscaleLambda.zip", json_string)
