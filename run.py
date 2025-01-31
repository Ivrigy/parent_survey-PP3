# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Import Libraries necessary for functioning of code 
import gspread
from google.oauth2.service_account import Credentials 
import os 
import re
import time


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

# Defining menu options and handling execution
class MenuOptions:
    def __init__(self, index, option, action_message, execute_action):
        self.index = index
        self.option = option
        self.action_message = action_message
        self.execute_action = execute_action

    def run_select_option(self):
        print(self.action_message)
        return self.execute_action()

    def display_menu_options(self):
        return f"\033[94m{self.index}\033[0m - {self.option}"


# Clearing screen function for better readability and decluttering
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Caling title sections
def display_title(title):
    print(f"\n{'-' * 80}")
    print(f"{title.center(80)}")
    print(f"{'-' * 80}\n")

# Displays menu options
def display_options(menu_options):
    for option in menu_options:
        print(f"\033[94m{option.index}\033[0m - {option.option}".ljust(40))
        
# Function that takes user inputed choice
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
            print(f"\033[91mAn unexpected error occurred: {e}\033[0m")

# Function to enter your data into survey
def access_survey():
    time.sleep(2)
    clear_screen()
    display_title("SHARE YOUR EXPERIENCE")
    survey_responses = {}
    
    for question, answers in QUESTION_OPTIONS.items():
        print(f"\n{question}")
        print()
        for index, answer in enumerate(answers, start=1):
            print(f"\033[94m{index}\033[0m - {answer}")
        
        choice = get_user_choice(answers)
        survey_responses[question] = answers[choice - 1]
    print("\nThank you for the feedback.")
    time.sleep(4)
    clear_screen()
   
    print("Here's a summary of your responses:\n")
    for question, selected_answer in survey_responses.items():
        print(question)
        print((f"  --> {selected_answer.upper()}\n"))

    update_worksheet(survey_responses, SURVEY)
    post_survey_action()

# Updating google sheet with new user answers
def update_worksheet(survey_responses, worksheet):
    try:
        responses_list = list(survey_responses.values())
        worksheet.append_row(responses_list)
        print("\nThank you, your answers have been recorded!\n")
    except Exception as e:
        print(f"\033[91mError updating worksheet: {e}\033[0m")

# Analysis Menu
def display_analysis_menu():
    display_title("ANALYSIS MENU")
    display_options(ANALYSIS_MENU)
    choice = get_user_choice(ANALYSIS_MENU)
    select_option = ANALYSIS_MENU[choice - 1]
    select_option.run_select_option()

# Statistical calculation and display of results
def summary_statistic():
    display_title("SUMMARY STATISTIC")
    headers, rows, total_answers = get_survey_data()
    if total_answers == 0:
        print("No survey responses found.")
        return
    survey_data = {}
    print(f"We received a total of {total_answers} responses.")
    for index, header in enumerate(headers):
        answers = [row[index] for row in rows]
        answer_count = {}
        for answer in answers:
            answer_count[answer] = answer_count.get(answer, 0) + 1
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

# Menu that comes after survey 
def post_survey_action():
    time.sleep(3)
    clear_screen()
    display_title("WHAT WOULD YOU LIKE TO DO NEXT?")
    display_options(POST_SURVEY_MENU)
    choice = get_user_choice(POST_SURVEY_MENU)
    select_option = POST_SURVEY_MENU[choice - 1]
    select_option.run_select_option()

def post_survey_clear_action():
    # print("." * 80)
    # print("\nWhat would you like to do next? Choose option:\n")
    display_title("WHAT WOULD YOU LIKE TO DO NEXT?")
    display_options(POST_SURVEY_CLEAR_MENU)
    choice = get_user_choice(POST_SURVEY_CLEAR_MENU)
    select_option = POST_SURVEY_CLEAR_MENU[choice - 1]
    select_option.run_select_option()

# Function that enables clearing of entry
def clear_last_entry():
    rows = SURVEY.get_all_values()
    if len(rows) > 1:
        SURVEY.delete_rows(len(rows))
        print("Your last entry has been cleared.")
    else:
        print("There are no entries to clear.")
    post_survey_clear_action()

# Fetching of survey data
def get_survey_data():
    data = SURVEY.get_all_values()
    headers = data[0]
    rows = data[1:]
    total_answers = len(rows)
    return headers, rows, total_answers

# Function to collect emails from users
def collect_email():
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        email = input("Please enter your email address (or type 'back' to return to the main menu): ").strip()
        if email.lower() == 'back':
            display_main_menu()
            return
        if re.match(email_regex, email):
            EMAIL_SHEET.append_row([email])
            print("Thank you! Your email has been recorded.")

            time.sleep(3)
            break
        else:
            print("Invalid email format. Please try again.")
    display_main_menu()

# Quiting and exiting function
def quit():
    print("\nThank you for participating!")
    print("Goodbye!")
    exit()

# Main Logic of the program
def display_main_menu():
    time.sleep(3)
    clear_screen()
    display_title("MAIN MENU")
    display_options(MAIN_MENU)
    choice = get_user_choice([option.option for option in MAIN_MENU])
    select_option = MAIN_MENU[choice - 1]
    select_option.run_select_option()

# Defining different menu options that appear after different functions
# Main and initaila menu
MAIN_MENU = [
    MenuOptions(1, "Enter Survey", "Entering single parent survey...\n", access_survey),
    MenuOptions(2, "Enter Analysis", "Entering Analysis of surveys...\n", display_analysis_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]
# Menu for statistics / analysis
ANALYSIS_MENU = [
    MenuOptions(1, "Summary Statistic", "Entering statistics...\n", summary_statistic),
    MenuOptions(2, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]
# Menu after submitting survey
POST_SURVEY_MENU = [
    MenuOptions(1, "Clear last survey entry", "Clearing last entry...\n", clear_last_entry),
    MenuOptions(2, "Enter Analysis", "Entering Analysis of surveys...\n", display_analysis_menu),
    MenuOptions(3, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(4, "Exit", "Exiting Program...", quit),
]
# Menu after clearing your survey entry
POST_SURVEY_CLEAR_MENU = [
    MenuOptions(1, "Enter Email to get updates", "Collecting email address...\n", collect_email),
    MenuOptions(2, "Back to Main Menu", "Entering main menu...\n", display_main_menu),
    MenuOptions(3, "Exit", "Exiting Program...", quit),
]


# Enter and run the program
if __name__ == "__main__":
    print("\nHello dear single parent!\n")
    print("Welcome to our online survey.")
    print("We value your feedback and assure you identity will remain completely anonymous.")
    print("In case if you wish that we get back to you, please leave your Email ")
    time.sleep(8)
    display_main_menu()