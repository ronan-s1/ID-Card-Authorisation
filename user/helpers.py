import qrcode
from user import constants as c
import uuid
import csv

def create_user_code(data):
    name, id = data
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 10)

    qr.add_data(f"name: {data[0]}\nID: {data[1]}")
    qr.make(fit = True)

    img = qr.make_image(fill = "black" , back_color = "white")
    img.save(c.CODE_PATH + f"{name}-{id}.png")


def add_user():
    row = [input("Enter Name: "), str(uuid.uuid1())[:6]]

    with open(c.VALID_USERS_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    create_user_code(row)