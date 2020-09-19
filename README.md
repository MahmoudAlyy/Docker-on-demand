# Docker-on-demand
Dockerized Django V2 web application to launch docker instances and interact with them using CLI.



The user can browse available images scraped from docker hub

![Imgur](https://i.imgur.com/sZETM12.png)



And launch one or more instances at the same time
(Ex: Launching Alpine & Python containers)

![Imgur](https://i.imgur.com/sYhiiIz.png)

# Installation

```
git clone https://github.com/MahmoudAlyy/Docker-on-demand
```
```
docker build -t docker_on_demand Docker-on-demand/.
````
```
docker run  -p 8000:8000 -it -v "/var/run/docker.sock:/var/run/docker.sock:rw" docker_on_demand
```
