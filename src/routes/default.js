import { spawn } from 'child_process';

function validate_request_format(reqBody) {
    if (!reqBody.hasOwnProperty('device_id')) {
        console.log('ERROR: Missing device_id field');
        return false;
    }
    if (!reqBody.hasOwnProperty('sensors')) {
        console.log('ERROR: Missing sensors field');
        return false;
    }
    // if (!reqBody.hasOwnProperty("pastFrames")) {
    //     return false;
    // }

    if (typeof reqBody['device_id'] != 'string') {
        console.log(
            'ERROR: Invalid device_id type: %s',
            typeof reqBody['device_id']
        );
        return false;
    }

    var ret = true;
    const sensors = reqBody['sensors'];
    if (sensors && sensors.length > 0) {
        sensors.forEach(function (sensor) {
            const data = sensor['data'];
            if (data && data.length > 0) {
                data.forEach(function (value) {
                    if (typeof value != 'number') {
                        console.log(
                            'ERROR: Invalid sensor value type: %s',
                            typeof value
                        );
                        ret = false;
                        return;
                    }
                });
            } else {
                console.log('ERROR: Sensor data array is empty');
                ret = false;
                return;
            }
            // TODO check if location string exists in map
            if (typeof sensor['location'] != 'string') {
                console.log(
                    'ERROR: Invalid sensor location type: %s',
                    typeof sensor['location']
                );
                ret = false;
                return;
            }
        });
    } else {
        console.log('ERROR: Sensors array is empty');
        return false;
    }

    return ret;
}

function handle_req(req, res) {
    console.log(req);
    if (validate_request_format(req.body)) {
        res.status(400);
        res.send('Invalid request body format'); // TODO return validation error message
    } else {
        var pythonData;

        // spawn new child process to call the python script
        const python = spawn('python3', [
            './src/scripts/Server.py',
            JSON.stringify(req.body)
        ]);

        // collect data from script
        python.stdout.setEncoding('utf8');
        python.stdout.on('data', function (data) {
            // console.log('Pipe data from python script ...');
            // console.log(data)
            pythonData = data.toString();
        });

        // check for error outputs
        python.stderr.setEncoding('utf8');
        python.stderr.on('data', function (data) {
            console.log('ERROR: ' + data);

            pythonData = data.toString();
        });

        // in close event we are sure that stream is from child process is closed
        python.on('close', (code) => {
            console.log(`child process close all stdio with code ${code}`);
            // send data to browser
            res.send(JSON.stringify(pythonData));
        });
    }
}

function handle_heartrate(req, res) {
    var pythonData;

    const python = spawn('python3', [
        './src/scripts/DemoServer.py',
        JSON.stringify(req.body)
    ]);

    // collect data from script
    python.stdout.setEncoding('utf8');
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        // console.log(data)
        pythonData = data.toString();
    });

    // check for error outputs
    python.stderr.setEncoding('utf8');
    python.stderr.on('data', function (data) {
        console.log('ERROR: ' + data);

        pythonData = data.toString();
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(JSON.stringify(pythonData));
    });
}

function handle_detect(req, res) {
    var pythonData;

    // spawn new child process to call the python script
    const python = spawn('python3', [
        './src/scripts/Server.py',
        './src/data/CAData.json',
        req.body[0]
    ]);

    // collect data from script
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        pythonData = data.toString().split('\n');
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send({
            heartRate: pythonData[0],
            ca: pythonData[1]
        });
    });
}

export { validate_request_format, handle_req, handle_heartrate, handle_detect };
