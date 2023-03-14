const express = require('express')
const {spawn} = require('child_process');
const app = express()
const port = 3000

app.use(express.json());
app.post('/', (req, res) => {
    var pythonData;
    
    // spawn new child process to call the python script
    const python = spawn('python3', ['Server.py', JSON.stringify(req.body)]);

    // collect data from script
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        pythonData = data.toString().split("\n");
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
    	res.send({
            heartRate: pythonData[0],
            ca: pythonData[1]
        })
    });
})

app.post('/healthy', (req, res) => {
    var pythonData;
    
    // spawn new child process to call the python script
    const python = spawn('python3', ['Server.py', 'data/healthyData.json', req.body[0]]);

    // collect data from script
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        pythonData = data.toString().split("\n");
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
    	res.send({
            heartRate: pythonData[0],
            ca: pythonData[1]
        })
    });
})

app.post('/ca', (req, res) => {
    var pythonData;
    
    // spawn new child process to call the python script
    const python = spawn('python3', ['Server.py', 'data/CAData.json', req.body[0]]);

    // collect data from script
    python.stdout.on('data', function (data) {
        // console.log('Pipe data from python script ...');
        pythonData = data.toString().split("\n");
    });

    // in close event we are sure that stream is from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
    	res.send({
            heartRate: pythonData[0],
            ca: pythonData[1]
        })
    });
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
