# epdmagic
Prepare your pictures for displaying on Spectra 6 (E6) colour E-Ink displays!

## What is it?
A docker microservice which will accept a binary image or URL and do the following:
- Rotate to best fit the target orientation.
- Downscale (keep aspect ratio) to target dimentions.
- Quantize in accordance to Spectra 6 E-Ink display colours (Black, White, Green, Blue, Red, Yellow).
- Dither to finalise and make the final picture presentable.

This was originally written to offload some of the heavy image manipulation from the ESP32-S3 on the [ESP32-S3-PhotoPainter 7.3inch E6 Full Color E-paper Display](https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter). It can be used for any project involving self-hosted smart E-Ink displays (e.g. Nextcloud integration).

## Usage
1. Install a suitable version of docker for your system as per the [official docs](https://docs.docker.com/engine/install/). If you are on Linux and want to use docker-compose or [portainer](https://docs.portainer.io/start/install-ce/server/docker/linux#introduction), you must also [install the docker-compose plugin](https://docs.docker.com/compose/install/linux/#install-using-the-repository). Windows users **don't** need to install compose separately.
2. Head to the [releases](https://github.com/gsec0/epdmagic/releases) page and download the latest epdmagic.tar image.
3. Load the image using `docker load -i epdmagic.tar`. *Or build image from the included `Dockerfile`. See release notes at the [releases](https://github.com/gsec0/epdmagic/releases) page for more info.*
4. Confirm the image is loaded with `docker images`.
5. If you're using portainer: (skip if not)
	1. Head over to **Portainer -> Stacks -> Add stack**
	2. Use the following docker compose to deploy the stack.
```
services:
  epdmagic:
    image: epdmagic:latest
    container_name: epdmagic
    ports:
      - 9600:8000
    restart: unless-stopped
```
6. If you're using standalone docker, you have two options: (skip if not):

**Option 1 - docker-compose**

Create a directory for the container.
```bash
$ mkdir epdmagic && cd ./epdmagic
```

Paste the compose example from step 5 and save it as `compose.yml`.
```bash
$ nano compose.yml
```

Run the container.
```bash
$ docker-compose up -d
```
**Option 2 - docker run**

Simply run this command to start the container.
```bash
$ docker run -d -p 9600:8000 --name epdmagic epdmagic:latest
```
7. Access the service on port `9600` (if using above configuration). **See below for usage examples.**

### Convert image from URL
```
curl -X 'POST' 'http://{your_ip}:9600/convert?url=https://cdn.creazilla.com/illustrations/6672281/claude-monet-adolphe-monet-in-the-garden-of-le-coteau-at-sainte-adresse-1867-ill-lg.jpeg&width=800&height=480'
```

Response headers:
```
content-disposition: inline; filename=result.bmp 
content-length: {length}
content-type: image/bmp 
date: {date}
server: uvicorn 
```

### Convert image from base64 encoded URL
```
curl -X 'POST' 'http://{your_ip}:9600/convert?url=aHR0cHM6Ly9jZG4uY3JlYXppbGxhLmNvbS9pbGx1c3RyYXRpb25zLzY2NzIyODEvY2xhdWRlLW1vbmV0LWFkb2xwaGUtbW9uZXQtaW4tdGhlLWdhcmRlbi1vZi1sZS1jb3RlYXUtYXQtc2FpbnRlLWFkcmVzc2UtMTg2Ny1pbGwtbGcuanBlZw==&width=800&height=480'
```

Response headers:
```
content-disposition: inline; filename=result.bmp 
content-length: {length}
content-type: image/bmp 
date: {date}
server: uvicorn 
```

### Convert binary image
```
curl -X 'POST' 'http://{your_ip}:9600/convert?width=800&height=480' -H 'accept: */*' -H 'Content-Type: multipart/form-data' -F 'file=@{your_jpeg}.jpg;type=image/jpeg'
```

Response headers:
```
content-disposition: inline; filename=result.bmp 
content-length: {length}
content-type: image/bmp 
date: {date}
server: uvicorn 
```

### Swagger UI
The service can be tested quickly using Swagger UI which can be accessed at
```
http://{your_ip}:9600/docs
```

## Development
Any contribution is welcome!


1. Install Python 3.13

**Debian**
```bash
$ sudo apt update
$ sudo apt install python3.13
```
**Windows**

Visit https://www.python.org/downloads/

2. Clone this repository.
```bash
$ git clone https://github.com/gsec0/epdmagic
```
3. Enter the project directory and create a python environment.
```bash
$ cd ./epdmagic
$ python3.13 -m venv venv
```
4. Activate the python environment.

**Bash**
```bash
$ source ./venv/bin/activate
```
**PowerShell**
```powershell
> .\venv\Scripts\Activate.ps1
```
5. Install the requirements.
```bash
$ pip install -r requirements.txt
```
6. Run the script.
```bash
$ uvicorn main:app --reload
```