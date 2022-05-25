import datetime
from scanning import helpers as s
from users import helpers as u
import os

def clear_screen():
   os.system("cls"if os.name in ("nt", "dos") else "clear")


def menu():
   #gets the date and time and displays it to user
   width = 55
   now = datetime.datetime.now()
   today = datetime.datetime.today()
   opts = [line.split("\n")[0] for line in open("menu.txt", "r").readlines()]
   
   print("─" * width)
   print(f"{today:%d %B %Y} - {now.strftime('%H:%M')}".center(width))
   print("─" * width)
   print("ID Card Authentication".center(width))
   print("─" * width)
   
   for i, opt in enumerate(opts):
      print(f"{str(i):>7s}) {opt}")
   
   print("─" * width)
    

def main():  
   while True:
      clear_screen()
      menu()
      user_choice = input("\nChoose an option: ")
      
      if user_choice == "0":
         break
      
      elif user_choice == "1":
         s.cam_scan()
         
      elif user_choice == "2":
         u.create_user()
         
      elif user_choice == "3":
         s.img_scan()
      
      else:
         print("\nInvalid Input Try again")
      
      input("\nPress enter to continue...")


if __name__ == "__main__":
   main()
