import picamera, time, math, os

ROTATION = 90
CAMERA_RES_X = 1920
CAMERA_RES_Y = 1080
CAMERA_FPS = 1/20
# Duration should be in seconds
DURATION = 60 * 60 * 11
NUM_SHOTS = (DURATION * CAMERA_FPS)

with picamera.PiCamera() as camera:
  camera.rotation = ROTATION
  camera.resolution = (CAMERA_RES_X, CAMERA_RES_Y)
#  camera.awb_mode='off'
#  camera.iso=400
  camera.led=False
  camera.start_preview()
  try:
    series = math.floor(time.time() * 1000)
    os.makedirs('/data/' + str(series), exist_ok=True)
    for i, filename in enumerate(camera.capture_continuous('/data/' + str(series) + '/{counter:06d}.jpg',format='jpeg',quality=100)):
#      print(filename + ' out of ' + str(NUM_SHOTS))
      time.sleep(1/CAMERA_FPS)
      if i == NUM_SHOTS:
        break
  finally:
    camera.stop_preview()
