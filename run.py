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


class MenuOptions:
    def __init__(self, index, option, action_message, execute_action):
        self.index = index
        self.option = option
        self.action_message = action_message
        self.execute_action = execute_action

    def display_menu_options(self):
        return f"{self.index} - {self.option}"
 
    def run_select_option(self):  # Renamed from run_selected_option to match your usage
        print(self.action_message)
        return self.execute_action() 

def access_survey():
    print("Survey accessed.")

def display_analysis_menu():
    print("Analysis menu displayed.")

def quit():
    print("Goodbye!")
    exit()

MAIN_MENU = [
    MenuOptions(1, "Enter Survey", "Entering single parent survey...\n", access_survey),
    MenuOptions(2, "Enter Analysis", "Entering Analysis of surveys...\n", display_analysis_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]



def display_title(title):
    print(title)

def display_main_menu():
    display_title("MENU")
    display_options(MAIN_MENU)
    choice = get_user_choice(MAIN_MENU)
    select_option = MAIN_MENU[choice - 1] 
    select_option.run_select_option()

def display_options(menu_options):
    for option in menu_options:
        print(option.display_menu_options())

def get_user_choice(options):
    while True:
        try:
            user_input = input(f"\nPlease enter your choice (1-{len(options)}):\n").strip() 
            if user_input.isdigit(): 
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(f"Error: Choose a number between 1 and {len(options)}.")
            else:
                print("Enter a valid number")
        except Exception as e:
            # Handle any unexpected errors
            print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    display_main_menu()