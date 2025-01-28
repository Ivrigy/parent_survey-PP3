# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open ('parent_survey')

SURVEY = SHEET.worksheet("survey_responses")
EMAIL_SHEET = SHEET.worksheet("email_addresses")

def display_main_menu():
    display_title("MENU")
    display_options(MAIN_MENU)
    choice = get_user_choice(MAIN_MENU)
    select_option = MAIN_MENU[choice -1]
    select_option.run_select_option()

def display_options(menu_options):
    for option in menu_options:
        print(option.display_menu_options())

def get_user_choice(options):
    while True:
        try:
          user_input = input(f"\nPlease enter your choice (1-{len(options)}):\n").strip() #removing empty spaces
        if user_input.isdigit():
            choice = int(user_input)
        if 1<= choice <= len(options):
            return choice
            
        else:
            print(f"Error: Choose a number between 1 and {len(options)}.")
    else:
        print("Enter a valid number")



