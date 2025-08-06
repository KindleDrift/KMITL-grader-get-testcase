# get-testcase

A simple Python CLI tool to get testcases from the KMITL Programming Lab web.

*Note this tool does not get you the hidden testcase.*

## Installation

1. Git clone and cd into the repo
    ```
    git clone https://github.com/KindleDrift/get-testcase.git

    cd get-testcase
    ```

2. Create virtual environment and install the required packages
    ```
    python -m venv venv
    pip install -r requirements.txt
    ```

3. Rename the `.env.example` to `.env`
    ```
    mv .env.example .env
    ```

4. Edit the `.env` file, see Usage Guide below for more details.

## Usage Guide

### Environment Variables

`CI_SESSION` is your cookies session, if left empty the scraper program will prompt you for username and password or for session token

`USER_AGENT` is your preferred browser header.

`PYTHON_PROGRAM_PATH` is the path to your Python program that you want to check, starts from the parent of get-testcase directory.

`MARKDOWN_PATH` is the path to your generated testcase file

### Scraper

To run the program, simply run
```
python main.py
```

If `CI_SESSION` are provided, username and password prompt are skipped.

If `CI_SESSION` are not provided, you may enter your username and password or `ci_session` manually by typing `use_session_auth` into username prompt. You will be prompted for `ci_session` after the username prompt.

```
Enter your student ID: use_session_auth
```

### get-lab CLI

You can type `help` to get list of commands.

Example usage:

1. To add exercise 1 from lab 5
    ```
    add 5 1
    ```

2. To add exercise 1,2,3 from lab 2 and 3
    ```
    add 2,3 1,2,3
    ```

3. To remove exercise 2,3 from lab 1
    ```
    rm 1 2,3
    ```

4. To check, current exercise to import to markdown.
    ```
    check
    ```

5. When you're finished run `done`. (Note `exit` will exit the CLI and cancel operation)

### testcase-run

You'll have to manually edit your Python program path and testcases path in the `.env` file

After selecting a path, you can simply type `ptw` into your terminal to run `pytest-watch`

