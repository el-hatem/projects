// Setup empty JS object to act as endpoint for all routes
projectData = {};

// import packages
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');


// start express app
const app = express();

// setup middlewares
app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());
app.use(cors());
app.use(express.static('website'));


// start a server
const host = 'localhost';
const port = 3000;

const server = app.listen(port, host, () => {
	console.log(`${server}`);
	console.log('server has just started');
	console.log(`server is running at: http://${host}:${port}`);
});

// +------------------ setUp Routers -----------------+

app.post('/add', (request, response) => {
	const entry = request.body;

  	projectData['date'] = entry.date;
  	projectData['temp'] = entry.temp;
  	projectData['content'] = entry.content;

  	response.send(projectData);
})

app.get('/all', (request, response) => {
	response.send(projectData);
})