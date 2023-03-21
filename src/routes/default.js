import { spawn } from 'child_process';


function handle_req (req, res) {
    var pythonData;

    // spawn new child process to call the python script
    const python = spawn('python3', ['./scripts/Server.py', JSON.stringify(req.body)]);

    // collect data from script
    python.stdout.setEncoding('utf8');
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        // console.log(data)
        pythonData = data.toString().split('\n');
    });

    // check for error outputs
    python.stderr.setEncoding('utf8');
    python.stderr.on('data', function(data) {
        console.log('ERROR: ' + data);

        data=data.toString();
        scriptOutput+=data;
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

function handle_healthy(req, res) {
    var pythonData;

    // spawn new child process to call the python script
    const python = spawn('python3', [
        './scripts/Server.py',
        './data/healthyData.json',
        req.body[0]
    ]);

    // collect data from script
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        console.log(data)
        pythonData = data.toString().split('\n');
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        console.log(pythonData);
        // send data to browser
        res.send({
            heartRate: pythonData[0],
            ca: pythonData[1]
        });
    });
}

function handle_ca(req, res) {
    var pythonData;

    // spawn new child process to call the python script
    const python = spawn('python3', [
        './scripts/Server.py',
        './data/CAData.json',
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

export { handle_dummy, handle_req, handle_healthy, handle_ca };