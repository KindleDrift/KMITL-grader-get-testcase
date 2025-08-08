from bs4 import BeautifulSoup
import requests
import time
import pprint

DELAY_CONST = 1

class Exercise:
    def __init__(self, title, description, testcase):
        self.title = title
        self.description = description
        self.testcase = testcase

    def to_markdown_format(self):
        s = f"## {self.title}\n### Description:\n{self.description}"
        for no, case in enumerate(self.testcase):
            s += f"\n#### Testcase #{no + 1}\n```\n{case}\n```"

        return s        

    def __str__(self):
        s = f"Exercise Name: {self.title}\nDescription: {self.description}"
        for no, case in enumerate(self.testcase):
            s += f"\nTestcase #{no + 1}\n{case}"

        return s


def get_available_lab(web_url, session):
    exercise_home = f"{web_url}/student/exercise_home"

    available_lab_with_name = {}

    status_map = {
        "open": True,
        "closed": False
    }

    response = session.get(exercise_home)

    # with open("home.html", 'rb') as f:
    #     response = f.read()

    soup = BeautifulSoup(response.content, 'html.parser')

    # print(soup)

    table_body = soup.find('tbody')
    if table_body:
        table_rows = table_body.find_all('tr')

        for row in table_rows:
            # Skip the bottom table
            if row.find('td', colspan=True):
                continue
            
            cols = row.find_all('td')
            
            lab_no = cols[0].get_text().strip()
            lab_name = cols[1].get_text().strip().replace(' View ONLY', '')
            is_open = status_map.get(cols[2].get_text().strip())

            if is_open:
                available_lab_with_name[lab_no] = lab_name

    pprint.pprint(available_lab_with_name)
    return available_lab_with_name


def get_lab_exercise(web_url, lab_exercise_to_get, session):
    exercise_page = f"{web_url}/student/lab_exercise"

    available_lab = get_available_lab(web_url, session)
    
    time.sleep(DELAY_CONST)
    for lab, exercises in lab_exercise_to_get.items():
        if lab in available_lab:
            for exercise in exercises:
                time.sleep(DELAY_CONST * 2)
                yield lab, available_lab.get(lab), exercise, get_exercise_info(f"{exercise_page}/{lab}/{exercise}", session)
        else:
            print(f"Skipping lab: {lab} including exercise {exercises} in the lab. [Error: Lab is closed]")


def get_exercise_info(web_url, session):
    response = session.get(web_url)

    # with open("KCE_DS_Student.html", 'rb') as f:
    #     response = f.read()

    soup = BeautifulSoup(response.content, 'html.parser')

    question_title = soup.find('h2').get_text()
    description = soup.find('div', class_="panel-body").get_text()
    testcases = soup.find_all('textarea')

    filtered_testcases = [
        testcase for testcase in testcases if 'id' not in testcase.attrs or testcase['id'] != 'sourcecode_content'
    ]

    test_list = []
    for testcase in filtered_testcases:
        test_list.append(testcase.get_text())
    
    return Exercise(question_title, description, test_list)


if __name__ == "__main__":
    print("hello")