from bs4 import BeautifulSoup
import requests


def get_login_session(web_url, payload, session):
    auth_url = f"{web_url}/Auth"

    response = session.post(auth_url, data=payload)

    soup = BeautifulSoup(response.content, 'html.parser')

    text_content = ""

    if response.status_code == 200:
        alert_div = soup.find('div', class_='alert')
        if alert_div:
            text_content = alert_div.text.strip()
        if "Username or password is invalid" in text_content:
            print("Username or password is invalid")
            return None
        elif "gay_burger" in text_content:
            print("Broken Yee")
            return None
        else:
            session_id = session.cookies.get('ci_session')
            print(f"Session ID: {session_id}")
            return session
    else:
        print(f"Login failed with status code: {response.status_code}")
        print(response.text)
        return None