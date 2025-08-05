from getpass import getpass
from bs4 import BeautifulSoup
from authenticate import get_login_session
from fetch_exercises import get_lab_exercise
import requests
import pprint
from pathlib import Path

def get_user_info():
    username = input("Enter your student ID: ")
    password = getpass("Enter your password: ")

    auth_payload = {
        "username": username,
        "password": password,
    }

    return auth_payload


def get_wanted_lab():
    lab_ex_to_get = {}
    while True:
        commands = ['exit', 'add', 'rm', 'check', 'done', 'help']
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
            case _:
                print("Unknown commands specified, type \"help\" for list of commands")


def main():
    custom_user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0"
    init_url = "https://python.compro.kmitl.ac.th/25s1ood/index.php"

    auth_payload = get_user_info()

    headers = {
        'User-Agent': custom_user_agent
    }

    session = get_login_session(init_url, auth_payload, headers=headers)

    if session:
        print("Login Success, now getting exercise question and testcase")
    else:
        print("Login Failed")
        return "FAIL"

    lab_ex_to_get = get_wanted_lab()

    for lab_no, lab, ex_no, exercise in get_lab_exercise("https://python.compro.kmitl.ac.th/25s1ood/index.php", lab_ex_to_get, session):
        s = f"# Lab: {lab}\n" + f"{exercise.to_markdown_format()}"
        new_dir = Path(f'ch{lab_no}')
        new_dir.mkdir(exist_ok=True)
        new_file = new_dir / f'ex0{ex_no}.md'
        new_file.write_text(s)


if __name__ == "__main__":
    main()

        
