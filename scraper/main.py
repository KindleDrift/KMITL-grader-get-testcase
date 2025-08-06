from getpass import getpass
from bs4 import BeautifulSoup
from authenticate import get_login_session
from fetch_exercises import get_lab_exercise
import requests
import pprint
from pathlib import Path
from dotenv import load_dotenv
import os

def get_user_info():
    username = input("Enter your student ID: ")
    if username == "use_session_auth":
        return getpass("Enter your ci_session: ")

    password = getpass("Enter your password: ")

    auth_payload = {
        "username": username,
        "password": password,
    }

    return auth_payload


def get_wanted_lab(session):
    lab_ex_to_get = {}
    while True:
        commands = ['exit', 'add', 'rm', 'check', 'done', 'help', 'get-sesskey']
        input_str = input("get-lab > ")

        command_input = input_str.strip().lower()
        formatted_command = command_input.split(' ')
        match formatted_command[0]:
            case "exit":
                print("Now exiting...")
                break
            case "help":
                print(f"List of availables command: {commands}")
                print(f"exit\t\t\t\texit without getting lab")
                print(f"help\t\t\t\tthis help tab")
                print(f"add [lab_no] [exercise_no]\tadd exercise no for the specified lab")
                print(f"rm  [lab_no] [exercise_no]\tremove lab exercise no for the specified lab")
                print(f"check\t\t\t\tgets the current exercise currently in the search check")
                print(f"done\t\t\t\tget the exercise")
                print(f"get-sesskey\t\t\tget the current session cookies")
            case "add":
                if len(formatted_command) != 3:
                    print("Invalid argument count for \"add\", add takes [lab_no] and [exercise_no]")
                else:
                    try:
                        arg_lab = list(map(int, formatted_command[1].split(',')))
                        arg_ex = list(map(int, formatted_command[2].split(',')))
                    except:
                        print("Invalid argument number format, [lab_no] and [exercise_no] takes an interger seperated by commas ','")

                    for lab in arg_lab:
                        key = str(lab)
                        if key not in lab_ex_to_get:
                            lab_ex_to_get[key] = []
                        
                        for ex in arg_ex:
                            if ex not in lab_ex_to_get[key]:
                                lab_ex_to_get[key].append(ex)

                        lab_ex_to_get[key].sort()
            case "rm":
                if len(formatted_command) != 3:
                    print("Invalid argument count for \"add\", add takes [lab_no] and [exercise_no]")
                else:
                    try:
                        arg_lab = list(map(int, formatted_command[1].split(',')))
                        arg_ex = list(map(int, formatted_command[2].split(',')))
                    except:
                        print("Invalid argument number format, [lab_no] and [exercise_no] takes an interger seperated by commas ','")

                for lab in arg_lab:
                    key = str(lab)
                    if key in lab_ex_to_get:
                        for ex in arg_ex:
                            if ex in lab_ex_to_get[key]:
                                lab_ex_to_get[key].remove(ex)
                        lab_ex_to_get[key].sort()
            case "check":
                pprint.pprint(lab_ex_to_get)
            case "done":
                print("Getting the exercise...")
                return lab_ex_to_get
            case "get-sesskey":
                print(session.cookies.get('ci_session'))
            case _:
                print("Unknown commands specified, type \"help\" for list of commands")


def main():
    load_dotenv()

    user_agent = os.getenv("USER_AGENT")
    init_url = "https://python.compro.kmitl.ac.th/25s1ood/index.php"

    auth_payload = None
    if not os.getenv("CI_SESSION"):
        auth_payload = get_user_info()
    else:
        auth_payload = str(os.getenv("CI_SESSION"))

    headers = {
        "User-Agent": f"{user_agent}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1", 
    }
    session = requests.Session()
    session.headers = headers
    
    if isinstance(auth_payload, dict):
        get_login_session(init_url, auth_payload, session)
        try: 
            if not session.cookies.get('ci_session'):
                # If ci_session is not obtained, try getting it again
                get_login_session(init_url, auth_payload, session)
        except:
            get_login_session(init_url, auth_payload, session)
        del auth_payload['password']
    else:
        session.cookies.set('ci_session', f'{auth_payload}')

    if session.cookies.get('ci_session'):
        res = session.get("https://python.compro.kmitl.ac.th/25s1ood/index.php/student/exercise_home")
        soup = BeautifulSoup(res.content, "html.parser")
        if soup.find("h4"):
            if soup.find("h4").text.strip() == "Access denied":
                print("ci_session is expired or something went wrong")
                return "CI_EXPIRED"
        print("Login Success")
    else:
        print("Login Failed")
        return "FAIL"

    lab_ex_to_get = get_wanted_lab(session)

    for lab_no, lab, ex_no, exercise in get_lab_exercise(init_url, lab_ex_to_get, session):
        s = f"# Lab: {lab}\n" + f"{exercise.to_markdown_format()}"
        new_dir = Path(f'../testcases/ch{lab_no}')
        new_dir.mkdir(parents=True, exist_ok=True)
        new_file = new_dir / f'ex0{ex_no}.md'
        new_file.write_text(s)


if __name__ == "__main__":
    main()

        
