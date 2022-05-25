import datetime
from scanning import helpers as s
from users import helpers as u
import os

def ClearConsole():
   os.system("cls"if os.name in ("nt", "dos") else "clear")

def menu():
   #gets the date and time and displays it to user
   width = 45
   now = datetime.datetime.now()
   today = datetime.datetime.today()
   opts = [line.split("\n")[0] for line in open("menu.txt", "r").readlines()]
   
   print("─" * width)
   print(f"{today:%d %B %Y} - {now.strftime('%H:%M')}".center(width))
   print("─" * width)
   print("Company ID Card Authentication".center(width))
   print("─" * width)
   
   for i, opt in enumerate(opts):
      print(f"{str(i + 1):>8s} {opt}")
   
   print("─" * width)
    
    


def main():
   # s.img_scan()
   # u.create_user()
   menu()
   # u.create_user()


if __name__ == "__main__":
    main()
