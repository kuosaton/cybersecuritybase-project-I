# cybersecuritybase-project-I

Submission for Cyber Security Base project I: https://cybersecuritybase.mooc.fi/module-3.1

Starter website created following Django's "Writing your first Django app" tutorial: https://docs.djangoproject.com/en/5.2/intro/

## Installation instructions

0. Ensure you have Django and Python installed
   - The application has been tested using Python versions `3.10.12` & `3.13.17` and Django `5.2.5`
   - Installation guide: https://cybersecuritybase.mooc.fi/installation-guide
2. Clone this repository to a location of your choice
3. Navigate to the repository's `src/` directory (`cybersecuritybase-project-I/src`) in shell
4. Run `python manage.py makemigrations` and `python manage.py migrate` to make necessary preparations
    - (If `python`doesn't work, try running the commands using `python3`)
```shell
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py makemigrations
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py
```
5. Start the server by running `python manage.py runserver`
```shell
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py runserver
```
6. After starting the server, navigate to its address in your browser (`http://127.0.0.1:8000/` by default).
```shell
Starting development server at http://127.0.0.1:8000/
```
