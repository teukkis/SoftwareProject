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
  `cd remoteChipWhiperer`
  `pip install -e .`
  `flask init-db` (rewrite the existing database)
  `flask testgen` (rewrite...)

5. Start the app
  `flask run`

### Frontend

1. Install node.js by running "sudo apt install nodejs" in terminal
2. install npm by running command "sudo apt install npm"
2. npm install ( npm rebuild if didn't work)
3. npm start in dir frontend


Database:
|virtual_machine |student        |
|----------------|---------------|
|id              |id             |
|user            |connect_time   |
|                |disconnect_time|
|                |password       |
