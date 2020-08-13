const express = require('express');

const dishRouter = express.Router();

dishRouter.route('/').all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','text/plain');
    next();
})
.get((req, res, next) => {
    res.end('Will send all the dishes to you.');
})
.post((req, res, next) => {
    res.end('Will add the dish ' + req.body.name + 
        ' with details: ' + req.body.description);
})
.put((req, res, next) => {
    res.statusCode = 403;
    res.end('PUT operation not supported on /dishes');
})
.delete((req, res, next) => {
    res.end('Deleting all the dishes!');
});


dishRouter.route('/:dishId').all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','text/plain');
    next();
})
.get((req, res, next) => {
    res.write('Details of the dish ' + req.body.name);
    res.end(' are:\n' + req.params.description);
})
.post((req, res, next) => {
    res.statusCode = 403;
    res.end('POST operation not supported on /dishes/'
    + req.params.dishId);
})
.put((req, res, next) => {
    res.write('Updating dish: ' + req.params.dishId + '\n');
    res.end('Will update the dish ' + req.body.name 
    + ' with details ' + req.body.description);
})
.delete((req, res, next) => {
    res.end('Deleting dish ' + req.body.name);
});

module.exports = dishRouter;