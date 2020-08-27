const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const auth = require('../authenticate');
const cors = require('./cors');
var Favorites = require('../models/favorites');
const { application } = require('express');

//Adjusting to MongoDB + NodeJS updates
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useUnifiedTopology', true);
mongoose.set('useCreateIndex', true);

var favoriteRouter = express.Router();

favoriteRouter.use(bodyParser.json());

favoriteRouter.route('/')
.options(cors.corsWithOptions, (req, res) => {
    res.sendStatus(200);
    res.contentType('application/json');
})
.get(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOne({user:req.user._id})
    .populate('dishes.dish')
    .populate('user')
    .then((favorite) => { 
        if (favorite != null) {
            res.json(favorite);
        }
        else {
            res.end('There are no favorites yet!')
        }
    }, 
        (err) => next(err))
    .catch((err) => next(err));
})
.post(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOne({user:req.user._id})
    .populate('user')
    .populate('dishes.dish')
    .then((favorite) => {
        if (favorite != null){
            for (let newIdIndex = 0; newIdIndex < req.body.length; newIdIndex++)
            {
                if (favorite.dishes.id(req.body[newIdIndex]._id) == null) {
                    
                    //Adding only dishes that werent favorites
                    favorite.dishes.push(req.body[newIdIndex]._id);
                }
            };
            favorite.save()          
            .then((favorite) => {
                res.json(favorite);
            }, (err) => next(err));
                
        } else {
            Favorites.create({user: req.user._id, dishes: req.body})
            .then((favorite) => {
                Favorites.findById(favorite._id)
                .populate('user')
                .populate('dishes.dish')
                .then((favorite) => {res.json(favorite)},
                    (err) => next(err));
            }, (err) => next(err))
        }
    }, (err) => next(err))
    .catch((err) => next(err));
})
.put(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.contentType('text/plain');
    res.end('PUT operation is not supported.');
})
.delete(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOneAndDelete({user:req.user._id})
    .then((favorite) => {
        res.json(deleted); 
    }, (err) => next(err))
    .catch((err) => next(err));
});

favoriteRouter.route('/:dishId')
.options(cors.corsWithOptions, (req, res) => {
    res.sendStatus(200);
    res.contentType('application/json');
})
.get(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOne({user: req.user._id})
    .then((favorites) => {
        if (!favorites) {
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            return res.json({"exists": false, "favorites": favorites});
        }
        else {
            if (favorites.dishes.indexOf(req.params.dishId) < 0) {
                res.statusCode = 200;
                res.setHeader('Content-Type', 'application/json');
                return res.json({"exists": false, "favorites": favorites});
            }
            else {
                res.statusCode = 200;
                res.setHeader('Content-Type', 'application/json');
                return res.json({"exists": true, "favorites": favorites});
            }
        }

    }, (err) => next(err))
    .catch((err) => next(err))
})
.post(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOne({user:req.user._id})
    .then((favorite) => {
        if (favorite != null && favorite.dishes.id(req.params.dishId) == null)
        {
            favorite.dishes.push(req.params.dishId);
            favorite.save()            
            .then((favorite) => {
                Favorites.findById(favorite._id)
                .populate('user')
                .populate('dishes.dish')
                .then((favorite) => {res.json(favorite)},
                    (err) => next(err));
            }, (err) => next(err));
        } else if ((favorite != null) && 
        (favorite.dishes.id(req.params.dishId) != null)) 
        {
            res.end('This dish is already on your list.\n');
        } else {
            Favorites.create({user: req.user._id})
            .then((favorite) => {
                favorite.dishes.push(req.params.dishId);
                favorite.save()
                .then((favorite) => {
                    Favorites.findById(favorite._id)
                    .populate('user')
                    .populate('dishes.dish')
                    .then((favorite) => {res.json(favorite)},
                    (err) => next(err));
                })
            }, (err) => next(err))
        }
    }, (err) => next(err))
    .catch((err) => next(err));
})
.put(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    res.statusCode = 403;
    res.contentType('text/plain');
    res.end('Operation is not supported.');
})
.delete(cors.corsWithOptions, auth.verifyUser, (req, res, next) => {
    Favorites.findOne({user:req.user._id})
    .then((favorite) => {
        if (favorite != null && favorite.dishes.id(req.params.dishId) != null)
        {
            favorite.dishes.id(req.params.dishId).remove();
            favorite.save()
            .then((deleted) => {
                Favorites.findById(deleted._id)
                .populate('user')
                .populate('dishes.dish')
                .then((deleted) => {res.json(deleted)},
                (err) => next(err));
            }, (err) => next(err));
        } 
        else if((favorite != null) && (favorite.dishes.id(req.params.dishId) == null)) 
        {
            res.end('This dish is not on your favorite list.')
        } 
        else 
        {
            res.end('Your favorite list is still empty.')
        }
    }, (err) => next(err))
    .catch((err) => next(err));
})

module.exports = favoriteRouter;