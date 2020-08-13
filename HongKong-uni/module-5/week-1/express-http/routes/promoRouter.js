const express = require('express');

const promoRouter = express.Router();

promoRouter.route('/').all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','text/plain');
    next();
})
.get((req, res, next) => {
    res.end('Will send all promotions to you.');
})
.post((req, res, next) => {
    res.end('Will add the promotion ' + req.body.name + 
        ' with details: ' + req.body.description);
})
.put((req, res, next) => {
    res.statusCode = 403;
    res.end('PUT operation not supported on /promotions');
})
.delete((req, res, next) => {
    res.end('Deleting all promotions!');
});


promoRouter.route('/:promoId')
.all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','text/plain');
    next();
})
.get((req, res, next) => {
    res.write('Details of the promotion ' + req.body.name);
    res.end(' are:\n' + req.params.description);
})
.post((req, res, next) => {
    res.statusCode = 403;
    res.end('POST operation not supported on /promotions/'
    + req.params.promoId);
})
.put((req, res, next) => {
    res.write('Updating promotion: ' + req.params.promoId + '\n');
    res.end('Will update the promotion ' + req.body.name 
    + ' with details ' + req.body.description);
})
.delete((req, res, next) => {
    res.end('Deleting promotion ' + req.body.name);
});

module.exports = promoRouter;