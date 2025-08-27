# Cyber Security Base project I

Submission for Cyber Security Base project I: https://cybersecuritybase.mooc.fi/module-3.1.

Starter website created following Django's "Writing your first Django app" tutorial: https://docs.djangoproject.com/en/5.2/intro/.

Project report with detailed flaw descriptions & flaw testing and fixing instructions: https://drive.proton.me/urls/24XF4JG9WM#k3eYJGvVAKi1

Screenshots of flaws before and after applying fixes: [screenshots](screenshots)

## About

This a simple polls application with the following features:
- Register and login
- Create and delete polls
- View polls, vote on them, and see vote results

## Installation instructions

1. Ensure you have Django and Python installed.
   - The application has been tested using Python versions `3.10.12` & `3.13.17` and Django version `5.2.5`.
   - Installation guide: https://cybersecuritybase.mooc.fi/installation-guide.

2. Clone this repository to a location of your choice.
3. Navigate to the repository's `src` directory (`/cybersecuritybase-project-I/src`) in shell.
4. Run `python manage.py migrate` to make necessary preparations.
   - If `python`doesn't work, try running the commands using `python3` instead.
6. Start the server by running `python manage.py runserver`.
7. Navigate to the server's address in your browser (`http://127.0.0.1:8000/` by default).
8. The app is ready!
