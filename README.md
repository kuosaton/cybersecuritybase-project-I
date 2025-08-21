# cybersecuritybase-project-I

Submission for [Cyber Security Base project I](https://cybersecuritybase.mooc.fi/module-3.1)

## Installation instructions

0. Ensure you have Django and Python installed
   -  Installation guide: https://cybersecuritybase.mooc.fi/installation-guide
1. Clone this repository to a location of your choice
2. Navigate to the repository's `src/` directory (`cybersecuritybase-project-I/src`) in shell
3. Run `python manage.py makemigrations` and `python manage.py migrate` to make necessary preparations
    - (If `python`doesn't work, try running the commands using `python3`)
```shell
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py makemigrations
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py
```
5. Start the server by running `python manage.py runserver`
```shell
kuosaton:~/csb/cybersecuritybase-project-I/src$ python manage.py runserver
```
6. After starting the server, navigate to its address in your which by default is `http://127.0.0.1:8000/`. Navigate to this address in your browser
```shell
Starting development server at http://127.0.0.1:8000/
```
