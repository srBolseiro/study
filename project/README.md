# SHIRE_RPG

SHIRE_RPG is a python based web application that allows rpg players to create and save their playersheets for games like WoD: Vampire the Masquerade 5th edition.

### 🚀 Tired of never finding a way to quickly create and save your rpg sheets when playing online?  
SHIRE_RPG intends to solve it. Just create an account, create your sheet under our supported games and open it anywhere!  
Since it's web-based, you can find it [@HERE](https://bagginsbr.pythonanywhere.com/)

## Online usage:
📦 Access https://bagginsbr.pythonanywhere.com/
🔩 Register your account under the website's database.  
🔩 Log in and navigate to player sheets.
🔩 Hit create and select the game template.  
🔩 Fill in all requested data and save!  
❤️ Now your character sheet shows on player sheets for you to acess!  

## 🔧 Local host: 
📌 First you'll need to place the contents of /project inside a python ready virtual machine.   
📌 The following instructions are for Linux, yet may apply to Windows using WSL.
Then, run:
```bash
.venv/bin/activate
```
```bash
pip3 install Flask
```
```bash
pip3 install cs50
```
```bash
pip3 install flask-session
```
## ⚙️ If everything is installed, go to app.py directory and run:
```bash
flask run
```
### 🛠️ Now repeat the steps as if you were online!


## 🛠️ Built using:

* [Flask](https://flask.palletsprojects.com/en/3.0.x/) - Web framework for python.
* [SQLite3](https://www.sqlite.org/) - Database handler.
* [python-cs50](https://github.com/cs50/python-cs50) - CS50 library for Python.
