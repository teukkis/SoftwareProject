### Backend

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

1. Install node.js
2. npm install ( npm rebuild if didn't work)
3. npm start in dir frontend


Database:
|virtual_machine |student        |
|----------------|---------------|
|id              |id             |
|user            |connect_time   |
|                |disconnect_time|
