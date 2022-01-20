docker ps; 
docker kill $(docker ps -q);
docker pull thefebrin/clouds:latest;
docker image list;
DEV=prod docker run --rm --name web-app-1 -p 2137:5000 -d -e DEV thefebrin/clouds:latest;
DEV=staging docker run --rm --name web-app-2 -p 2138:5000 -d -e DEV thefebrin/clouds:latest;
DEV=error docker run --rm --name web-app-3 -p 2139:5000 -d -e DEV thefebrin/clouds:latest;
docker ps;