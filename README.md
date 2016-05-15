1. https://docs.docker.com/linux/step_one/
2. Add yourself to docker group : sudo usermod -aG docker kvasukib
3. check docker is running : sudo service docker status
4. docker run hello-world : To check if docker is working correctly

To Run the script:
python dockerInterface.py --zip grayscaleLambda.zip --name grayscaleLambda --cmd "python ./lambdaMain.py MM.mp4 MM.mp4" --image "ubuntu:14.04"
