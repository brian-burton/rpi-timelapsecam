# rpi-timelapsecam
Raspberry Pi camera + Node-Red based timelapse camera

I'm toying with timelapse photography on my RPi + NoIR camera.

## Prerequisites
- A Raspberry Pi running [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
- Node-Red: RPi installation instructions are [here](http://nodered.org/docs/hardware/raspberrypi)
- node-red-dashboard: Details are [here](https://www.npmjs.com/package/node-red-dashboard)

## Structure of the repo
I'm using the Export/Library feature in Node-Red, with the git folder symlinked to that.
- **System** is full of stuff that I use for managing the Pi itself
- **Camera** is the stuff that takes pictures
