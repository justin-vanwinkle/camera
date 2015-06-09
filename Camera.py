import time
import RPi.GPIO as GPIO
import picamera
from datetime import datetime

camera = picamera.PiCamera()
        

def main():
        
    #GPIO setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 1
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 2
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 3
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button 4
    GPIO.add_event_detect(16, GPIO.FALLING)
    GPIO.add_event_detect(15, GPIO.FALLING)
    GPIO.add_event_detect(13, GPIO.FALLING)
    GPIO.add_event_detect(12, GPIO.FALLING)

    nFrame = 1.0
    nZoomInterval = 1.001
    bRecording = False

    #camera settings
    camera.resolution = (1920,1080)
    camera.framerate = 30
    camera.mode = 1
    camera.video_stabilization = True
    camera.video_denoise = True
    camera.sharpness = 100
    camera.iso = 100
    camera.brightness = 55
    camera.annotate_text = "Primal Ops, L.L.C."
    
    camera.start_preview()

        
    while(1):
        time.sleep(0.01)
        #record
        if GPIO.event_detected(16):
            if bRecording:
                bRecording = False
                camera.stop_recording()
                return()
            else:
                bRecording = True
                strDateTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')
                strFilename = strDateTime + "Spotlight.mkv" 
                camera.start_recording(strFilename, format='h264', resize=None, bitrate=0, quality=25)
        #no zoom
        elif GPIO.event_detected(15):
            nFrame = 1
            camera.zoom = (0.0,0.0,1.0,1.0)
        #zoom out
        elif GPIO.event_detected(13):
            while GPIO.input(13) == GPIO.LOW:
                if nFrame <= 1:
                    nFrame *= nZoomInterval
                    corner = 0.5 - nFrame/2.0
                    camera.zoom = (corner,corner,nFrame,nFrame)
                    #time.sleep(0.01)
        #zoom in
        elif GPIO.event_detected(12):
            while GPIO.input(12) == GPIO.LOW:
                if nFrame >= 0.2:
                    nFrame /= nZoomInterval
                    corner = 0.5 - nFrame/2.0            
                    camera.zoom = (corner,corner,nFrame,nFrame)
                    #time.sleep(0.003)
                    print(nFrame)
        
main()
