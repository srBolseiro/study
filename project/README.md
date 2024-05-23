# SHIRE_RPG
### SHIRE_RPG is a python based web application that allows rpg players to create and save their playersheets for games like WoD: Vampire the Masquerade 5th edition.
#### Video Demo: [VIDEO]()

## Online usage:
📦 Access https://bagginsbr.pythonanywhere.com/  
🔩 Register your account under the website's database.  
🔩 Log in and navigate to player sheets.  
🔩 Hit create and select the game template.  
🔩 Fill in all requested data and save!  
❤️ Now your character sheet shows on player sheets for you to acess!  

### 🚀 Tired of never finding a way to quickly create and save your rpg sheets when playing online?  
SHIRE_RPG intends to solve it. Just create an account, create your sheet under our supported games and open it anywhere!  
Since it's web-based, you can find it [HERE](https://bagginsbr.pythonanywhere.com/)

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

# Boring technical app details:
## Authentication:
Uses standard python library "werkzeug.security". Requires username sized between 4 and 20 chars and password sized between 8 and 16 chars.  
Doesn't require much more security due to low sensitivity of data. Doesn't refuse connection after few attempts (to be implemented).  
Uses either html form checking for pattern and server side verification.  
All content require a session, except home page generic view.  

## Pages:  
### Home:
Displays the currently supported games and player characters.  
Current supported games, yet it's dinamically generated, doesn't come from a database, but from a python list inside "app.py". I've done it this way so I keep closer control of available game sheets.  
Player sheets come from a database query that verify characters/game linked to user_id.  
### Player Sheets:  
Has a dropdown menu with dinamic generated input. Lists all character/game linked to user_id.  
Has "pick", "create" and "delete" options.  
📌 If create is selected, user'll be redirected to a creation environment.  
📌 If pick is selected, user'll be redirected to the sheet rendered -> edit is yet to be implemented!!!!!!  
📌 If delete is selected, user'll be redirected to a deletion environment.  
### Creation environment:
Each game has a unique sheet style. Each sheet has its own table inside the database.  
The support for a game demands the html template design and table creation. The python function might be reused, just have to change some names.  
It is required (and server verified) to fill "character name" and "player name" because those are the table keys used to query.  
Once user clicks on "save", the server check every information filled and insert into the table if no other user AND character AND game match.
### Editing:
*Not implemented yet, sorry!*  
### Profile:
User may change password if needed.
### Login
*If user forgets password, he'll have to contact support*  
The python code for lenghts is as follows:
```bash
if len(username) < 4 or len(username) > 20 or len(password) < 8 or len(password) > 16:
```

### 📌 Project’s title: SHIRE_RPG  
### 📌 My name: Yuri A  
### 📌 GitHub: srBolseiro  
### 📌 edX: yurigregorio  
### 📌 Location: São Pedro, São Paulo, Brazil  
and, the date you have recorded this video.
