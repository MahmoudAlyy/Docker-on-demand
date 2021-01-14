# Docker-on-demand
Dockerized Django V2 web application to launch docker instances and interact with them using Shell.



The user can browse available images scraped from docker hub,

![Imgur](https://i.imgur.com/NLtNDyG.png)


launch one or more instances

(Ex: Launching Alpine & Python containers)

![Imgur](https://i.imgur.com/gCg0nwY.png)


and view, attach or kill running containers.

![Imgur](https://i.imgur.com/nVibthb.png)

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
## Note
Long running tasks and interactive commands doesn't work.
