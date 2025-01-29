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
        return f"\033[94m{self.index}\033[0m - {self.option}"
 
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
    print(f"\n*** {title} ***\n")

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
            user_input = input(f"\nPlease enter your choice (\033[94m1-{len(options)}\033[0m):\n").strip() 
            if user_input.isdigit(): 
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(f"\033[91mError: Choose a number between 1 and {len(options)}.\033[0m")
            else:
                print("\033[91mEnter a valid number.\033[0m")
        except Exception as e:
            # Handle any unexpected errors
            print(f"\033[91mAn unexpected error occurred: {e}\033[0m")



if __name__ == "__main__":
    display_main_menu()