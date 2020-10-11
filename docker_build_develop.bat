cd docker_ffmpeg
docker build -f Dockerfile-buster -t blthayer/ffmpeg:buster .
docker build -f Dockerfile-slim -t blthayer/ffmpeg:slim .
cd ..\
docker build -f Dockerfile-develop -t blthayer/disquip-bot:develop .