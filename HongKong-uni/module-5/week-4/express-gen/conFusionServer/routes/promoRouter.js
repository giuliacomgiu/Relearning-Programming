const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const Promos = require('../models/promotions');
var auth = require('../authenticate');
const cors = require('./cors');

//Adjusting to MongoDB + NodeJS updates
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useUnifiedTopology', true);
mongoose.set('useCreateIndex', true);


const promoRouter = express.Router();

promoRouter.use(bodyParser.json());

//Hanling all promotions
promoRouter.route('/')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req, res, next) => {
    Promos.find(req.query)
    .then(
        (promos) => res.json(promos), 
        (err) => next(err))
    .catch((err) => next(err));
})
.post(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    Promos.create(req.body)
    .then (
        (promo) => res.json(promo), 
        (err) => next(err))
    .catch((err) => next(err));
})
.put(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    res.statusCode = 403;
    res.setHeader('Content-Type','text/plain');
    res.end('PUT operation not supported on /promotions');
})
.delete(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    Promos.deleteMany({})
    .then(
        (resp) => res.json(resp), 
        (err) => next(err))
    .catch((err) => next(err));
});


//Handling specific promotion
promoRouter.route('/:promoId')
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get(cors.cors, (req, res, next) => {
    Promos.findById(req.params.promoId)
    .then(
        (promo) => res.json(promo),
        (err) => next(err))
    .catch((err) => next(err));
})
.post(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    res.statusCode = 403;
    res.end('POST operation not supported on /promotions/'
    + req.params.promoId);
})
.put(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    Promos.findByIdAndUpdate(req.params.promoId,
        { $set: req.body }, 
        { new:true })
    .then(
        (promo) => res.json(promo),
        (err) => next(err))
    .catch((err) => next(err));
})
.delete(cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
    (req, res, next) => 
{
    Promos.findByIdAndDelete(req.params.promoId)
    .then(
        (resp) => res.json(resp),
        (err) => next(err))
    .catch((err) => next(err));
});

module.exports = promoRouter;