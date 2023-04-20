# Codeblue Server
Node server code for running detection algorithm Python scripts on EC2 server


## Setup
1. Create a new Firebase project using the [Firebase console](https://console.firebase.google.com/)
2. Get the firebase private key file and place it under the root directory `/firebase-ppk.json`

## Running the server
```bash
python3 -m venv ./env # create Python virtual environment

source env/bin/activate # activate Python virtual environment

npm i # install express library

pip install -r requirements.txt # install python dependencies

npm start # start node server
```

**NOTE:** Consider using [PM2](https://pm2.keymetrics.io/docs/usage/quick-start/) to allow server to always be running. 

## Message formats
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
