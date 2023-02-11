# Codeblue Server

Node server code for running detection algorithm Python scripts on EC2 server

### Running the server
On EC2: 
```bash
python3 -m venv ./env # create Python virtual environment

source env/bin/activate # activate Python virtual environment

npm i # install express library

pip install -r requirements.txt # install python dependencies

node index.js # start node server
```

### Requirements
- [ ] firebase private key `firebase-ppk.json` file
- [ ] replace `device_fcm_token` in `Server.py` with the token in simulator terminal output 