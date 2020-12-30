## Admin tools
### Backend

First install python 3 virtual environment
python3 -m pip install --user virtualenv

1. Create virtual machine 
  `python3 -m venv /path/to/virtualenv`

2. Activate the machine
  `source /path/to/the/virtualenv/bin/activate`

3. Set env
  `export FLASK_APP=backend`
  `export FLASK_ENV=development`

4. Setup 
  `pip install -e .`

5. Start the app
  `flask run`

### Frontend

1. Install node.js by running "sudo apt install nodejs" in terminal
2. install npm by running command "sudo apt install npm"
2. npm install ( npm rebuild if didn't work)
3. npm start in dir frontend

## User frontend/backend instructions
https://docs.google.com/document/d/1eLq4cELIre191PyiXXTQSmdhI9Q_1StRKt-wmhKU3dY/edit?usp=sharing


Database:
|virtual_machine |student        |
|----------------|---------------|
|id              |id             |
|user            |connect_time   |
|                |disconnect_time|
|                |password       |
