#! /usr/bin/python3

import picamera
import time
import math
import os
import argparse

from syslog import syslog
from sys import exit

def arghandler():
    parser = argparse.ArgumentParser(description='Take a single picture with the Pi Camera',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-y', '--height', default=1080, type=int, help='the height of the frame')
    parser.add_argument('-x', '--width', default=1920, type=int, help='the width of the frame')
    parser.add_argument('-i', '--interval', default = 10.0, type=float, help='the time between frames in seconds')
    parser.add_argument('-d', '--duration', default = 10, type=int, help='the length of time to record in seconds')
    parser.add_argument('-r', '--rotation', default = 0, type=int, help='rotation of the output image (0, 90, 180, 270)')
    return parser.parse_args()

def taketheshot(width: int, height: int, rotation: int, interval: float, duration: int):
    """Take multiple shots. If the interval between shots is long, shutdown to save power"""
    shots = math.ceil(duration/interval)
    series = math.floor(time.time() * 1000)
    os.makedirs('/data/' + str(series), exist_ok=True)
    KEEPCAMHOT = True if (interval < 5) else False
    WARMUPTIME = 2

    with picamera.PiCamera() as camera:
        camera.rotation = rotation
        camera.resolution = (width, height)
        #  camera.awb_mode='off'
        #  camera.iso=400
        camera.led=False

        if KEEPCAMHOT:
            camera.start_preview(resolution = (width,height))
            time.sleep(WARMUPTIME)
            try:
                for i, filename in enumerate(camera.capture_continuous('/data/' + str(series) + '/{counter:06d}.jpg',format='jpeg',quality=80)):
                    if i == shots:
                        break
                    time.sleep(interval)
            finally:
                camera.stop_preview()
        else:
            for i in range(shots + 1):
                camera.start_preview(resolution = (width,height))
                time.sleep(WARMUPTIME)
                camera.capture('/data/' + str(series) + f'/{i:06d}.jpg',format='jpeg',quality=80)
                camera.stop_preview()
                if i < shots:
                    time.sleep(interval - WARMUPTIME)

def main():
    args = arghandler()
    #syslog(args)
    #print(args)
    if args.duration < args.interval:
        #syslog(f"Duration ({args.duration}s) cannot be less than interval between shots ({args.interval}s)")
        print(f"Duration ({args.duration}s) cannot be less than interval between shots ({args.interval}s)")
        exit(1)
    taketheshot(args.width, args.height, args.rotation, args.interval, args.duration)

if __name__ == "__main__":
    main()
