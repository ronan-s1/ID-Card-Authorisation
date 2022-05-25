import cv2
import numpy as np
import pandas as pd
from pyzbar.pyzbar import decode
from users import constants as c

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    
    data = pd.read_csv(c.USERS_PATH)
    user_ids = data["id"].tolist()
    
    for obj in barcode:
        points = obj.polygon
        
        x, y, w, h = obj.rect
        
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))

        barcode_data = obj.data.decode("utf-8")
        barcode_type = obj.type
        
        id_from_code = barcode_data.split(",")[0]
        
        
        if id_from_code in user_ids:
            string = "Valid"
            colour = (0, 255, 0)
        else:
            string = "Invalid"
            colour = (0, 0, 255)

        cv2.polylines(image, [pts], True, colour, 3)
        cv2.putText(image, string, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)
        
        print(f"{barcode_data} - {barcode_type}")


def cam_scan():
    #initialise web cam
    cap = cv2.VideoCapture(0)
    while True:
        #getting frames from web cam
        ret, frame = cap.read()
        decoder(frame)
        
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break


def img_scan():
    code_img = cv2.imread(f"{c.CODE_PATH}o-e17060.png")
    code_img_resize = cv2.resize(code_img, (827, 1170))
    
    decoder(code_img_resize)
    cv2.imshow("image", code_img_resize) 
    cv2.waitKey(0)

