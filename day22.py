from day18 import login_user
from day21 import citizen_menu
from day15 import connect_database

username = input("Enter username: ")
password = input("Enter password: ")

citizen_id = login_user(username, password)

if citizen_id:
    print("Welcome to Citizen Portal")
    citizen_menu(citizen_id)
else:
    print("Login failed")