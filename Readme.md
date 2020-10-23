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

  