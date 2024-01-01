// Require Statements
const express = require("express");
const app = express();
const port = 6969;
const morgan = require("morgan");
require('dotenv').config();
const cors = require("cors");

// CORS
app.use(cors());

// To send Data to the client
var bodyParser = require('body-parser');
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

app.use(morgan('dev'))

let target_clients = 5;
let clients = 0;
let callbacks = [];
let data = [];

function addArrays(arr1, arr2) {
    const result = [];

    for (let i = 0; i < arr1.length; i++) {
        const innerResult = [];

        for (let j = 0; j < arr1[i].length; j++) {
            if (Array.isArray(arr1[i][j])) {
                // Add corresponding elements of nested arrays
                const sum = arr1[i][j].map((value, index) => value + arr2[i][j][index]);
                innerResult.push(sum);
            } else {
                // Add corresponding elements of non-nested arrays
                innerResult.push(arr1[i][j] + arr2[i][j]);
            }
        }

        result.push(innerResult);
    }

    return result;
}

// Function to add arrays of arrays
function addArrayOfArrays(arrays) {
    if (arrays.length < 2) {
        return arrays[0];
    }

    let result = addArrays(arrays[0], arrays[1]);

    for (let i = 2; i < arrays.length; i++) {
        result = addArrays(result, arrays[i]);
    }

    return result;
}

// Function to divide each element by the number of arrays
function divideByCount(array, count) {
    return array.map((row) =>
        row.map((element) => (Array.isArray(element) ? element.map((value) => value / count) : element / count))
    );
}

function aggregate() {
    const dataArrays = [];
    for (let i = 0; i < data.length; i++) {
        dataArrays.push(data[i].map(item => JSON.parse(item)));
    }
    const resultArray = addArrayOfArrays(dataArrays);
    const numberOfArrays = dataArrays.length;

    // Divide each element by the number of arrays
    const finalResult = divideByCount(resultArray, numberOfArrays);
    return finalResult;
}

app.post("/api/v1/check", (req, res) => {
    data.push(req.body.params);
    clients++;
    if (clients === target_clients) {
        callbacks.push(response => res.send(response));
        let result = JSON.stringify(aggregate());
        callbacks.forEach(callback => callback({ result: result }));
        callbacks = [];
        clients = 0;
    } else {
        callbacks.push(response => res.send(response));
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});