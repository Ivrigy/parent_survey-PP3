# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Import Libraries necessary for functioning of code 
import gspread
from google.oauth2.service_account import Credentials 
import os 
import re

# Defining scope with help of Love Sandwiches
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# Credentials improved after refractoring
try:
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('parent_survey')
    SURVEY = SHEET.worksheet("survey_responses")
    EMAIL_SHEET = SHEET.worksheet("email_addresses")
except Exception as e:
    print(f"\033[91mError connecting to Google Sheets: {e}\033[0m")
    exit()

# Defining survey questions and answers
QUESTION_OPTIONS = {
    "How satisfied are you with your current management of day to day life?": [
        "Very satisfied", "Satisfied", "Neither", "Dissatisfied", "Very Dissatisfied"
    ],
    "How satisfied are you with the communication to your ex-partner?": [
        "Very satisfied", "Satisfied", "Neither", "Dissatisfied", "Very Dissatisfied"
    ],
    "How easy is for you to seek for additional help?": [
        "Very easy", "Easy", "Neither", "Difficult", "Very Difficult"
    ],
    "How easy is for you to generate income and provide for your child/children?": [
        "Very easy", "Easy", "Neither", "Difficult", "Very Difficult"
    ],
    "How would you rate your current mental health?": [
        "Excellent", "Good", "Average", "Bad", "Terrible"
    ],
    "How would you rate your current physical health?": [
        "Excellent", "Good", "Average", "Bad", "Terrible"
    ]
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_title(title):
    print(f"\n{'-' * 80}")
    print(f"{title.center(80)}")
    print(f"{'-' * 80}\n")

def display_main_menu():
    display_title("MENU")
    display_options(MAIN_MENU)
    choice = get_user_choice([option.option for option in MAIN_MENU])
    select_option = MAIN_MENU[choice - 1] 
    select_option.run_select_option()

def display_options(menu_options):
    for option in menu_options:
        print(f"\033[94m{option.index}\033[0m - {option.option}".ljust(40))
        print()

class MenuOptions:
    def __init__(self, index, option, action_message, execute_action):
        self.index = index
        self.option = option
        self.action_message = action_message
        self.execute_action = execute_action
       
    def run_select_option(self):  # Renamed from run_selected_option to match your usage
        print(self.action_message)
        return self.execute_action()  

    def display_menu_options(self):
        return f"\033[94m{self.index}\033[0m - {self.option}"

def access_survey():
    display_title("SHARE YOUR EXPERIENCE")
    survey_responses = {}
    for question, answers in QUESTION_OPTIONS.items():
        print(f"\n{question}")
        for index, answer in enumerate(answers, start=1):
            print(f"{index} - {answer}")
        choice = get_user_choice(answers)
        survey_responses[question] = answers[choice - 1]
    print("\nYour feedback matters!\n".center(80))
    for question, selected_answer in survey_responses.items():
        print(question)
        print((f"  --> {selected_answer.upper()}\n"))
    update_worksheet(survey_responses, SURVEY)
    post_survey_action()

def update_worksheet(survey_responses,SURVEY):
    try:
        responses_list = list(survey_responses.values())
        SURVEY.append_row(responses_list)
        print("\nThank you, your answers have been recorded!\n".center(80))
    except Exception as e:
        print(f"\033[91mError updating worksheet: {e}\033[0m") 

def display_analysis_menu():
    display_title("ANALYSIS MENU")
    display_options(ANALYSIS_MENU)
    choice = get_user_choice(ANALYSIS_MENU)
    select_option = ANALYSIS_MENU[choice - 1]
    select_option.run_select_option()

def summary_statistic():
    display_title("SUMMARY STATISTIC")
    headers, rows, total_answers = get_survey_data()
    survey_data = {}
    print(f"We recieved total of {total_answers} responses")
    for index, header in enumerate(headers):
        answers = [row[index] for row in rows]
        answer_count = {}
        for answer in answers:
            answer_count[answer] = answer_count.get(answer,0) + 1
        survey_data[header] = { 
            answer: round((count / total_answers) * 100, 1)
            for answer, count in answer_count.items()
        }
    for question, answers in survey_data.items():
        print(f"\n{'-' * 80}")
        print(f"{question.upper().center(80)}")
        print(f"{'-' * 80}")
        for answer, percentage in answers.items():
            print(f"   --> {answer}: {percentage} %")
    post_survey_clear_action()

def post_survey_action():
    print("." * 80)
    print("What would you like to do next? Choose option:")
    display_options(POST_SURVEY_MENU)
    choice = get_user_choice(POST_SURVEY_MENU)
    select_option = POST_SURVEY_MENU[choice - 1]
    select_option.run_select_option()

def post_survey_clear_action():
    print("." * 80)
    print("What would you like to do next? Choose option:")
    display_options(POST_SURVEY_CLEAR_MENU)
    choice = get_user_choice(POST_SURVEY_CLEAR_MENU)
    select_option = POST_SURVEY_CLEAR_MENU[choice - 1]
    select_option.run_select_option()

def clear_last_entry():
    rows = SURVEY.get_all_values()
    if len(rows) > 1:
        SURVEY.delete_rows(len(rows))
        print("Your last entry has been cleared.")
    else:
        print("There are no entries to clear")
    post_survey_clear_action()

def get_survey_data():
    data = SURVEY.get_all_values()
    headers = data[0]
    rows = data[1:]
    total_answers = len(rows)
    return headers, rows, total_answers

def collect_email():
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        email = input("Please enter your email address: ")
        if re.match(email_regex, email):
            EMAIL_SHEET.append_row([email])
            print("Thank you! Your email has been recorded.")
            break
        else:
            print("Invalid email format. Please try again.")
    display_main_menu() 


def quit():
    print("Goodbye!")
    exit()


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



MAIN_MENU = [
    MenuOptions(1, "Enter Survey", "Entering single parent survey...\n", access_survey),
    MenuOptions(2, "Enter Analysis", "Entering Analysis of surveys...\n", display_analysis_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]

ANALYSIS_MENU = [
    MenuOptions(1, "Summary Statistic", "Entering statistics...\n", summary_statistic),
    MenuOptions(2, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]

POST_SURVEY_MENU = [
    MenuOptions(1, "Clear last survey entry", "Clearing last entry...\n", clear_last_entry),
    MenuOptions(2, "Enter Analysis", "Entering Analysis of surveys...\n", display_analysis_menu),
    MenuOptions(3, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(4, "Exit", "Exiting Program...", quit),
]

POST_SURVEY_CLEAR_MENU = [
    MenuOptions(1, "Enter Email to get updates", "Collecting email address...\n", collect_email),
    MenuOptions(2, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]

if __name__ == "__main__":
    display_main_menu()