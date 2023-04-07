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


### Request message format
```json
{
  "sensors": [
    {
      "data": [v1, v2, v3, ...],
      "location": "location"
    }, {
      "data": [...],
      "location": "..."
    }, {
      ...
    }, ...
  ],
  "pastFrames": [v(-1), v(-2), v(-3)],
  "device_id": "abc"
} 
```
Where:
- 'data' represents all signal values from the past 10-second frame. It contains at least 1 10-second interval, with points expected to be spaced at 0.02s apart.
- 'location' represents the corresponding confidence levels associated with each sensor location
- 'pastFrames' represents the estimated heart rate of previous 10 second frames.
    - 'pastFrames' can be empty, and hold up to a maximum of 3 values.

### Response message format
```json
{
  "heartRate": "60",
  "ca": "True"
} 
```
