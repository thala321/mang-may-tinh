'use strict'

const express = require('express')
const bodyParser = require('body-parser')
const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

// Create a new instance of express
const app = express()

// Tell express to use the body-parser middleware and to not parse extended bodies
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// Route that receives a POST request to /sms
app.get('/', function (req, res) {
    res.send(`Server`)
  })

// Route that receives a POST request to /sms
app.post('/data', function (req, res) {
  const image = req.body.image;
  var secret_key = "sk_DEMODEMODEMODEMODEMODEMO";
  var url = "https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=" + secret_key;
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);

  // Send POST data and display response
  xhr.send(image);
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
          const obj = JSON.parse(xhr.responseText);
          if (obj.results && obj.results.length) {
              console.log("Biển số xe:", obj.results[0].plate);
          }
      } else {
          console.log("Server received data");
      }
  }

  res.set('Content-Type', 'text/plain')
  res.send(`Received`)
})

// Tell our app to listen on port 3000
app.listen(3000, function (err) {
  if (err) {
    throw err
  }

  console.log('Server started on port 3000')
})