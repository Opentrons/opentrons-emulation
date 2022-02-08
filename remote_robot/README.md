docker build . -t github_remote_robot --build-arg ROBOT_URL=http://UNIQUE.ngrok.io

ROBOT_URL retrieved from logs of github action run.

docker run -p 31950:31950 github_remote_robot