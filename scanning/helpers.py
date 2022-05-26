import cv2
import glob
import numpy as np
import pandas as pd
from pyzbar.pyzbar import decode
from scanning import constants as c

#decoding barcodes
def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    
    data = pd.read_csv(c.VALID_USERS_PATH)
    user_ids = data["id"].tolist()
    
    #looking for barcodes
    for obj in barcode:
        points = obj.polygon
        
        x, y, w, h = obj.rect
        
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))

        barcode_data = obj.data.decode("utf-8")
        barcode_type = obj.type
        
        #getting user id from barcode
        id_from_code = barcode_data.split(",")[0]
        
        #if valid or not
        if id_from_code in user_ids:
            string = "Valid"
            colour = c.GREEN
            
        else:
            string = "Invalid"
            colour = c.RED

        #displaying data
        cv2.polylines(image, [pts], True, colour, 3)
        cv2.putText(image, string, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colour, 2)
        
        print(f"{barcode_data} - {barcode_type}")


#turns on camera
def cam_scan():
    #initialise web cam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        #getting frames from web cam
        ret, frame = cap.read()
        decoder(frame)
        
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            break


#scanning a particular ID
def img_scan():
    user_input, id_cards = choose_id()
    
    if user_input == 0:
        print("There are no ID cards!")
        return
    
    #opening chosen ID card
    code_img = cv2.imread(f"{c.ID_CARDS_PATH}{id_cards[user_input - 1]}")
    code_img_resize = cv2.resize(code_img, (c.W, c.H))
    print("")
    
    #decoding chosen qr code
    decoder(code_img_resize)
    cv2.imshow(f"ID card: {id_cards[user_input - 1][:-4]}", code_img_resize)
    print("\nPlease close the ID card window to continue")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def choose_id():
    #put file names in a list
    id_cards = [id.split("\\")[1] for id in glob.glob(f"{c.ID_CARDS_PATH}*")]
    print("")
    
    if len(id_cards) == 0:
        return 0, 0
    
    #iterating and printing the names of the files
    for i, id_card in enumerate(id_cards):
        print(f"{i + 1} -> {id_card[:-4]}")
    
    print("\nEnter the corresponding number for the ID")
    
    #error checking
    while True:
        user_input = input("\nEnter: ")
        
        try:
            int(user_input)
            if int(user_input) <= len(id_cards) and int(user_input) > 0:
                return int(user_input), id_cards
            
        except ValueError:
            pass
        
        print("\nInvalid input! Try again")
        