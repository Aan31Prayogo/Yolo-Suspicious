#import library dan file yang dibutuhkan
import time                      #library pewaktu
import cv2                       #library opencv
import threading                 #library multithreading
import os                        #library Operating system
import requests                  #library untuk http method
from datetime import datetime    #library date and time
import json                      #library json object
import torch                     #library for loading YOLOv5 model
import RPi.GPIO as GPIO            #library GPIO

# #deklarasi variabel GPIO
relay=3

#Deklarasi pin GPIO pada raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay, GPIO.OUT)        #RELAY Aktif low
GPIO.output(relay,0)

#path untuk save foto
PATH_CAPTURE = os.getcwd() + "/capture/"
PATH_MODEL = os.getcwd() + "/model/"

#deklarasi font untuk library opencv
font = cv2.FONT_HERSHEY_SIMPLEX

#deklarasi warna opencv
green_color = (0, 255, 0)
red_color = (0, 0, 255)
thickness = 2

#ukuran display camera
CAMERA_WIDTH = 240
CAMERA_HEIGHT = 240

#BOT TELEGRAM & MODEL CONFIG
config_file_path = os.getcwd() + '/config.json'
with open(config_file_path, 'r') as file:
    config_data = json.load(file)
    
BOT_TOKEN = config_data.get('BOT_TOKEN')
CHAT_ID = config_data.get('CHAT_ID')
MODEL = config_data.get('MODEL')

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=PATH_MODEL + MODEL, force_reload=True)


def start_send_image_to_telegram(file_img):
    t4 = threading.Thread(target=send_image_to_telegram, args=(file_img,))
    t4.start()

def send_image_to_telegram(file_img):    
    try:
        image = open(PATH_CAPTURE + file_img, 'rb')
        for id__ in CHAT_ID:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={id__}"
            resp = requests.get(url, files={'photo': image}) 
            if int(resp.status_code) == 200:
                print('success send to telegram')

    except Exception as e:
        print(f'[FAILED] send image to telegram with error = {e}')

def start_set_relay_active():
    # threading untuk menjalankan relay
    t1 = threading.Thread(target=set_relay_active)
    t1.start()
    
def set_relay_active():
    try:
        GPIO.output(relay, 1)  # aktif low untuk relay
        time.sleep(30)   # aktifkan relay selama 30 detik
        GPIO.output(relay, 0)  # kembalikan keadaan relay
    except Exception as e:
        print("error set relay with error =>" + str(e))
        
# def start_open_camera():
#   # threading untuk menjalankan kamera
#   t1 = threading.Thread(target=open_camera)
#   t1.start()

def open_camera():
    global frame
    # deklarasi variabel
    prev_frame_time = 0
    new_frame_time = 0
    
    try:
        print("start open camera")
        # membuat objek kamera
        cap = cv2.VideoCapture(0)
        cap.set(3, CAMERA_WIDTH)             # set resolusi (width) kamera
        cap.set(4, CAMERA_HEIGHT)            # set resolusi (height) kamera

        # looping pembacaan kamera
        while True:
            ret, frame = cap.read()
            
            if not ret:  # jika gagal membaca webcam 
                print('failed to open camera')
                break

            new_frame_time = time.time()
            fps = 1/(new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            fps = f"{fps:.2f}"
            
            results = model(frame, size=320)
            #results = model(frame)
            results.render()

            cv2.putText(frame, "fps:", (5, 20), font, 0.7, green_color, 2)
            cv2.putText(frame, fps, (50, 20), font, 0.7, green_color, 2)

            cv2.imshow('Camera Feed', frame)  # menampilkan feed camera
            key = cv2.waitKey(1) & 0xFF  # menganmbil keyboard event 
            
            if key == ord('q'):  # tekan q untuk exit
                break
            
            elif key == ord('c'):  # tekan c untuk capture
                capture_camera()
    
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"failed to open camera with error {e}")

def capture_camera():
    # fungsi untuk memfoto dengan kamera
    global frame
    
    try:        
        now = datetime.now()        # mengambil waktu saat ini
        dt_string = str(now.strftime("%d%m%Y_%H%M%S"))    # formating waktu
        pictName = dt_string + '.jpg'
        # frame = cv2.putText(frame, dt_string, (10, 200), font, 1, green_color, 2)
        cv2.imwrite(PATH_CAPTURE + pictName, frame)  # menyimpan foto di folder capture
        
        print(f'Capture image with name {pictName}')
        start_send_image_to_telegram(pictName)
    except Exception as e:
        print(f'[FAILED] to capture camera with error {e}')

# program utama 
if __name__ == '__main__':
    print("Program STARTING!!")
 
    if not os.path.exists(PATH_CAPTURE):
        os.mkdir(PATH_CAPTURE)
 
    open_camera()
