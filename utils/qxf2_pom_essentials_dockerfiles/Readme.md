# 🐳 Qxf2 Page Object Model (POM) Docker Setup with VNC Access

This Docker image sets up a Selenium testing environment with:

- Google Chrome
- Firefox
- XVFB (virtual display)
- x11vnc (VNC access to the GUI)
- Python 3.12 and virtual environment
- Sample tests to run selenium tests on Chrome and Firefox 

## Prerequisites

- Docker installed
- A VNC Viewer (e.g., TigerVNC, RealVNC, Remmina)

---

## Build the Docker Image

Run the following command in the directory where your `Dockerfile` is located:

```
docker build -t qxf2-pom-essentials:python3.12 .
```
---

## Pull image from Docker Hub:
You can also skip the build step and pull the pre-built image directly:
```
docker pull qxf2rohand/qxf2-pom-essentials:python3.12
```
View image at  https://hub.docker.com/r/qxf2rohand/qxf2_pom_essentials

---
##  Run the Docker Container
```
docker run -it -p 5999:5999 qxf2-pom-essentials:python3.12 /bin/bash
```
Port 5999 exposed for VNC access.

---

##  Connect via VNC
1. Open your VNC Viewer

2. Connect to:
```vncviewer localhost:99```

You’ll now see the browser UI inside your container.

---

## Run the Sample Test
Inside the Docker container terminal:
```
python sample_test_chrome.py
```
You’ll now see VNC viewer, it opens the chrome browser and navigates to https://www.qxf2.com and prints title.

---

## Note:
You can connect complete framework as a volume to container, install requirements, edit and run your tests.

---
