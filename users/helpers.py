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

#creating user's code
def create_qr_code(name, gender, user_id):
    qr = qrcode.QRCode(version = 1, box_size = 90)
    qr_code_path = c.CODE_PATH + f"{name}-{user_id}"
    
    qr.add_data(f"{user_id},{name},{gender}")
    qr.make(fit = True)

    img = qr.make_image(fill = "black" , back_color = "white")
    img.save(f"{qr_code_path}.png")
    
    creating_user_card(name, gender, qr_code_path)


#creating user's ID card 
def creating_user_card(name, gender, qr_code_path):
    #creating pdf object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size = 28)
    pdf.set_text_color(0, 60, 200)   
    
    #Possessive gramar checking
    if name[-1].lower() == "s":
        user_str = f"{name}' ID card"
    else:
        user_str = f"{name}'s ID card"
    
    #getting user's face
    response = requests.get(f"https://fakeface.rest/face/view?gender={gender}&minimum_age=25")
    image_bytes = io.BytesIO(response.content)
    PIL.Image.open(image_bytes).save(f"{c.CODE_PATH}face.png")
    
    #adding qr code and user's face to pdf
    pdf.cell(200, 30, txt = user_str, align = "C")
    pdf.image(f"{c.CODE_PATH}face.png", x=76, y=55, w=70)
    pdf.image(f"{qr_code_path}.png", x=76, y=130, w=70)
    pdf.output(f"{qr_code_path}.pdf")
    
    #converting pdf to png
    converted_img = convert_from_path(f"{qr_code_path}.pdf")
    for image in converted_img:
        image.save(f"{qr_code_path}.png")
    
    #removing everything but the ID card
    os.remove(f"{c.CODE_PATH}face.png")
    os.remove(f"{qr_code_path}.pdf")
    
    print("\nDone!")
         

#creating new user
def create_user():
    name = input("Name: ")
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
    with open(c.USERS_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    create_qr_code(name, gender, user_id)