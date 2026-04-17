# Docker Lab 1 Observations

**1. What is the size of your image? Is it large or small — and why do you think that is?**
The size of my `nginx:alpine` image is relatively small, showing as 93.5MB in my `docker images` list and about 26MB compressed in `docker inspect`. It is small because it is based on Alpine Linux, a very lightweight and minimal distribution designed specifically for containers, which excludes unnecessary packages and heavy libraries commonly found in full operating system distributions.

**2. How many layers does your image have? What does each major layer add?**
According to the `docker inspect` output, the image's `RootFS` section has 8 layers. Based on the `docker image history` output, the major layers primarily add the following:
- ~9.11 MB: The base Alpine Linux root filesystem (minirootfs).
- ~5.59 MB: Creation of the necessary nginx user and group.
- ~51.8 MB: The core Nginx installation and its dependencies.
- Several smaller KB layers: Various configuration scripts and docker entrypoint shell files (like `10-listen-on-ipv6-by-default.sh` and `docker-entrypoint.sh`).

**3. What operating system and architecture does your image use? (from docker inspect)**
From the `docker inspect` output, the image uses the **`linux`** operating system and the **`amd64`** architecture.

**4. Nginx: What does the port mapping -p 8080:80 actually mean? What would happen if you used -p 9090:80 instead?**
The port mapping `-p 8080:80` connects port `8080` on my host machine (my Mac) to port `80` inside the Docker container, where Nginx is listening. If I used `-p 9090:80` instead, Nginx would still securely run on port 80 inside the container, but I would need to access it via `http://localhost:9090` from my web browser to connect from the outside.

**5. In one paragraph: what surprised you most about this lab?**
What surprised me most was how quickly and seamlessly an entire web server could be spun up locally. Without having to install heavy dependencies, navigate complex permissions, or configure Nginx manually on my host system, a single `docker run` command provided a fully isolated, functional server environment in under a second.
