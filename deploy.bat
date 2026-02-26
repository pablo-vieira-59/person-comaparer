docker build -t facenet-app .
docker rm -f facenet-app
docker run -d -p 8000:8000 --name facenet-app --restart unless-stopped facenet-app