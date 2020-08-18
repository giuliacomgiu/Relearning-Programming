const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const Leaders = require('../models/leaders');
var authenticate = require('../authenticate');

//Adjusting to MongoDB + NodeJS updates
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useUnifiedTopology', true);
mongoose.set('useCreateIndex', true);


const leaderRouter = express.Router();

leaderRouter.use(bodyParser.json());

//Handling all leaders
leaderRouter.route('/')
.all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','application/json');
    next();
})
.get((req, res, next) => {
    Leaders.find({})
    .then(
        (leaders) => res.json(leaders), 
        (err) => next(err))
    .catch((err) => next(err));
})
.post(authenticate.verifyUser, (req, res, next) => {
    Leaders.create(req.body)
    .then (
        (leader) => res.json(leader), 
        (err) => next(err))
    .catch((err) => next(err));
})
.put(authenticate.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.setHeader('Content-Type','text/plain');
    res.end('PUT operation not supported on /leadertions');
})
.delete(authenticate.verifyUser, (req, res, next) => {
    Leaders.deleteMany({})
    .then(
        (resp) => res.json(resp), 
        (err) => next(err))
    .catch((err) => next(err));
});


//Handling specific leader
leaderRouter.route('/:leaderId')
.all((req, res, next) => {
    res.statusCode = 200;
    res.setHeader('Content-Type','application/json');
    next();
})
.get((req, res, next) => {
    Leaders.findById(req.params.leaderId)
    .then(
        (leader) => res.json(leader),
        (err) => next(err))
    .catch((err) => next(err));
})
.post(authenticate.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.end('POST operation not supported on /leadertions/'
    + req.params.leaderId);
})
.put(authenticate.verifyUser, (req, res, next) => {
    Leaders.findByIdAndUpdate(req.params.leaderId,
        { $set: req.body }, 
        { new:true })
    .then(
        (leader) => res.json(leader),
        (err) => next(err))
    .catch((err) => next(err));
})
.delete(authenticate.verifyUser, (req, res, next) => {
    Leaders.findByIdAndDelete(req.params.leaderId)
    .then(
        (resp) => res.json(resp),
        (err) => next(err))
    .catch((err) => next(err));
});

module.exports = leaderRouter;