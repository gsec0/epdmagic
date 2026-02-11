# epdmagic
Prepare your pictures for displaying on Spectra 6 (E6) colour E-Ink displays!

## What is it?
A docker microservice which will accept a binary image or URL and do the following:
- Downscale (keep aspect ratio) to **800 × 480**.
- Quantize in accordance to Spectra 6 E-Ink display colours (Black, White, Green, Blue, Red, Yellow).
- Dither to finalise and make the final picture presentable.

This was originally written to offload some of the heavy image manipulation from the ESP32-S3 on the [ESP32-S3-PhotoPainter 7.3inch E6 Full Color E-paper Display](https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter). It can be used for any project involving self-hosted smart E-Ink displays (e.g. Nextcloud integration).

## Usage
1. Install a suitable version of docker for your system as per the [official docs](https://docs.docker.com/engine/install/).
2. Head to the [releases](https://github.com/gsec0/epdmagic/releases) page and download the latest epdmagic.tar image.
3. Load the image using `docker load -i epdmagic.tar`.
4. Confirm the image is loaded with `docker images`.
5. If you're using portainer: (skip if not)
	- Head over to **Portainer -> Stacks -> Add stack**
	- Use the following docker compose to deploy the stack.
```
services:
  epdmagic:
    image: epdmagic:latest
    container_name: epdmagic
    ports:
      - 9600:8000
    restart: unless-stopped
```
6. If you're using standalone docker, you have two options: (skip if not)
	- If using docker-compose, create a directory on your machine called `epdmagic` and paste the docker compose example from step 5 into a `epdmagic/compose.yml` file. Change directory to `epdmagic` and run `docker-compose up -d`.
	- If using standalone docker, simply run `docker run -d -p 9600:8000 --name epdmagic epdmagic:latest`
7. Access the service on port `9600` (if using above configuration). See below for usage examples.

### Convert URL image
```
curl -X 'POST' 'http://{your_ip}:9600/convert?url=https://cdn.creazilla.com/illustrations/6672281/claude-monet-adolphe-monet-in-the-garden-of-le-coteau-at-sainte-adresse-1867-ill-lg.jpeg'
```

Response headers:
```
content-disposition: inline; filename=result.bmp 
content-length: {length}
content-type: image/bmp 
date: {date}
server: uvicorn 
```

### Convert base64 encoded URL
```
curl -X 'POST' 'http://{your_ip}:9600/convert?url=aHR0cHM6Ly9jZG4uY3JlYXppbGxhLmNvbS9pbGx1c3RyYXRpb25zLzY2NzIyODEvY2xhdWRlLW1vbmV0LWFkb2xwaGUtbW9uZXQtaW4tdGhlLWdhcmRlbi1vZi1sZS1jb3RlYXUtYXQtc2FpbnRlLWFkcmVzc2UtMTg2Ny1pbGwtbGcuanBlZw=='
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
curl -X 'POST' 'http://{your_ip}:9600/convert' -H 'accept: */*' -H 'Content-Type: multipart/form-data' -F 'file=@{your_jpeg}.jpg;type=image/jpeg'
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

Simply `git clone` this repo and create a Python 3.13 venv with `python -m venv venv` and install `/requirements.txt` file with `pip install -r requirements.txt`.