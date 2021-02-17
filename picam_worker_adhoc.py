#! /usr/bin/python3

import picamera
import time
import math
import os
import argparse

from syslog import syslog

def arghandler():
    parser = argparse.ArgumentParser(description='Take a single picture with the Pi Camera',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-y', '--height', default=1080, type=int, help='the height of the frame')
    parser.add_argument('-x', '--width', default=1920, type=int, help='the width of the frame')
    parser.add_argument('-i', '--interval', default = 10.0, type=float, help='the time between frames in seconds')
    parser.add_argument('-d', '--duration', default = 10, type=int, help='the length of time to record in seconds')
    parser.add_argument('-r', '--rotation', default = 0, type=int, help='rotation of the output image (0, 90, 180, 270)')
    return parser.parse_args()

def multishot():
    """Take multiple shots, keeping the camera running between frames for faster framerates"""
    with picamera.PiCamera() as camera:
        camera.rotation = ROTATION
        camera.resolution = (CAMERA_RES_X, CAMERA_RES_Y)
        #  camera.awb_mode='off'
        #  camera.iso=400
        camera.led=False
        camera.start_preview(resolution = (1920,1080))
        time.sleep(2)
        try:
            series = math.floor(time.time() * 1000)
            os.makedirs('/data/' + str(series), exist_ok=True)
            for i, filename in enumerate(camera.capture_continuous('/data/' + str(series) + '/{counter:06d}.jpg',format='jpeg',quality=80)):
                #print(filename + ' out of ' + str(NUM_SHOTS))
                time.sleep(1/CAMERA_FPS)
                if i == NUM_SHOTS:
                    break
        finally:
            camera.stop_preview()

def main():
    args = arghandler()
    print(args)
    ROTATION = args.rotation
    CAMERA_RES_X = args.width
    CAMERA_RES_Y = args.height
    CAMERA_FPS = 1 / args.interval
    DURATION = args.duration
    NUM_SHOTS = (DURATION * CAMERA_FPS)
    KEEPCAMHOT = True if (args.interval < 5) else False

    if KEEPCAMHOT:
        multishot()
#    else:
        # TODO: function to turn cam off between shots


if __name__ == "__main__":
    main()