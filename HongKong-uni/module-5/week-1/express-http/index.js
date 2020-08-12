const express = require('express'),
    http = require('http'),
    morgan = require('morgan'),
    bodyParser = require('body-parser')

const hostname = 'localhost';
const port = 3000;

const app = express();
app.use(morgan('dev'));
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());

app.all('/dishes', (req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','text/plain');
    next();
})

//OPERATION ON ALL DISHES
app.get('/dishes', (req, res, next) => {
    res.end('Will send all the dishes to you.');
});

app.post('/dishes', (req, res, next) => {
    res.end('Will add the dish ' + req.body.name + 
        ' with details: ' + req.body.description);
});

app.put('/dishes', (req, res, next) => {
    res.statusCode = 403;
    res.end('PUT operation not supported on /dishes');
});

app.delete('/dishes', (req, res, next) => {
    res.end('Deleting all the dishes!');
});

//OPERATION ON SPECIFIC DISH
app.get('/dishes/:dishId', (req, res, next) => {
    res.end('Will send the dishes of the dish: '
    + req.params.dishId);
});

app.post('/dishes/:dishId', (req, res, next) => {
    res.statusCode = 403;
    res.end('POST operation not supported on /dishes/'
    + req.params.dishId);
});

app.put('/dishes/:dishId', (req, res, next) => {
    res.write('Updating dish: ' + req.params.dishId + '\n');
    res.end('Will update the dish ' + req.body.name 
    + ' with details ' + req.body.description);
});

app.delete('/dishes/:dishId', (req, res, next) => {
    res.end('Deleting dish ' + req.body.name);
});

app.use((req, res, next) => {
    console.log(req.headers);
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end('<html><body><h1>This is an Express Server</h1></body></html>');

});

const server = http.createServer(app);

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});

/* Alternatively, could do
const server = http.createServer(app
    ).listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
}); */