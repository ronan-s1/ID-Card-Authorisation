from scanning import helpers as s
import io
import PIL
import requests
from users import constants as c
from fpdf import FPDF
from pdf2image import convert_from_path
import qrcode
import uuid
import os
import csv
import pandas as pd

#creating user's code
def create_qr_code(name, gender, user_id):
    qr = qrcode.QRCode(version = 1, box_size = 90)
    qr_ID_CARDS_PATH = c.ID_CARDS_PATH + f"{name}-{user_id}"
    
    qr.add_data(f"{user_id},{name},{gender}")
    qr.make(fit = True)

    img = qr.make_image(fill = "black" , back_color = "white")
    img.save(f"{qr_ID_CARDS_PATH}.png")
    
    creating_user_card(name, gender, qr_ID_CARDS_PATH)


#creating user's ID card 
def creating_user_card(name, gender, qr_ID_CARDS_PATH):
    #creating pdf object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size = 28)
    pdf.set_text_color(0, 60, 200)   
    
    #Possessive grammar checking
    if name[-1].lower() == "s":
        user_str = f"{name}' ID card"
    else:
        user_str = f"{name}'s ID card"
    
    #getting user's face
    response = requests.get(f"https://fakeface.rest/face/view?gender={gender}&minimum_age=25")
    image_bytes = io.BytesIO(response.content)
    PIL.Image.open(image_bytes).save(f"{c.ID_CARDS_PATH}face.png")
    
    #adding qr code and user's face to pdf
    pdf.cell(200, 30, txt = user_str, align = "C")
    pdf.image(f"{c.ID_CARDS_PATH}face.png", x=c.X, y=55, w=c.W)
    pdf.image(f"{qr_ID_CARDS_PATH}.png", x=c.X, y=130, w=c.W)
    pdf.output(f"{qr_ID_CARDS_PATH}.pdf")
    
    #converting pdf to png
    converted_img = convert_from_path(f"{qr_ID_CARDS_PATH}.pdf")
    for image in converted_img:
        image.save(f"{qr_ID_CARDS_PATH}.png")
    
    #removing everything but the ID card
    os.remove(f"{c.ID_CARDS_PATH}face.png")
    os.remove(f"{qr_ID_CARDS_PATH}.pdf")
    
    print("\nDone!")
         

#creating new user
def create_user():
    name = input("\nName: ")
    user_id = str(uuid.uuid1())[:6]
    
    #input validation stuff
    males = ["male", "m", "man"]
    females = ["female", "f", "woman"]
    
    while True:
        gender = input("Gender: ").lower()
        
        if gender in males:
            gender = "male"
            break
            
        elif gender in females:
            gender = "female"
            break
            
        else:
            print("\nInvalid input. Try again!\n")

    #loading display
    print("\nCreating ID card, please wait.")
    
    #adding info to csv
    row = [user_id, name, gender]
    with open(c.VALID_USERS_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    create_qr_code(name, gender, user_id)


#deleting user
def delete_user():
    #getting IDs in a list and error checking
    print("\nID cards you can delete:")
    user_input, id_cards = s.choose_id()
    
    if user_input == 0:
        print("There are no ID cards!")
        return
    
    #getting ID to delete and name from the file name
    delete_id = id_cards[user_input - 1].split("-")[1][:6]
    name = id_cards[user_input - 1].split("-")[0]
    data = pd.read_csv(c.VALID_USERS_PATH)
    all_user_ids = data["id"].tolist()
    
    #checking if ID is a verified ID
    if delete_id in all_user_ids:
        data =  data[data.id != delete_id]
        data.to_csv(c.VALID_USERS_PATH, index = False)
    
    #remove ID card from system
    os.remove(f"{c.ID_CARDS_PATH}{id_cards[user_input - 1]}")
    
    print(f"\n{name} has been deleted with ID {delete_id}")
    
        
    
    
    
    
   
