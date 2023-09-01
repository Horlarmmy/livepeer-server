# Use a base image with your desired operating system
FROM ubuntu:20.04

# Update the package list and install GStreamer and other dependencies
RUN apt-get update && \
    apt-get install -y gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly&& \
    apt-get clean

# Install Python and pip
RUN apt-get install -y python3 python3-pip
# Install Python dependencies
RUN pip install websockets

# Set the working directory
WORKDIR /app

# Copy your server code into the container (assuming your server code is in the same directory as the Dockerfile)
COPY . /app

# Specify the command to run when the container starts
CMD ["python3", "server.py"]
