# SeniorDesignProject
>-SSH Stetup<br/>
>-In .ssh<br/>
>-ssh-keygen -t rsa -b 4096 -C "SeniorDesign Isaiah Linux"<br/>
>-Then copy the generated id_rsa.pub<br/>
>-After adding key to github<br/>
>-Enter command in repo<br/>
>git remote set-url origin git@github.com:IsaiahST2020/SeniorDesignProject.git<br/>

## Setup with pipenv
To have this environment run as smoothly as possible, you can run the following commands to get a working setup for production or development

### Installing pipenv
to get all the dependencies independant of the system, you will need to install `pipenv`

debian/ubuntu:
```bash
sudo apt install pipenv
```
every other system
```bash
$ pip install pipenv
```
## Installing dependencies with pipenv
Once that is done, navigate to the workspace and run the following commands
```bash
$ pipenv install
```
### Installing dependencies + development libraries
This includes things like `pylint` and `autopep8` to help keep formatting and documentation consistent.
```bash

pipenv install --dev
```
## Running the application
if you want to run the server using the virtual environment provided by pipenv you can follow these steps on a fresh install
```bash
pipenv uninstall --all
pipenv install --dev
pipenv shell
sudo python3 -m pip install -r requirements.txt
pip freeze
mkdir data
cd data
touch db.sqlite3
cd ..
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py createsuperuser
sudo python3 manage.py runserver
```
or
```bash
pipenv shell 
exit (to leave shell)
```
