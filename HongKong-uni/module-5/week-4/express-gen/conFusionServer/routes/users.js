var express = require('express');
var router = express.Router();
const bodyParser = require('body-parser');
var User = require('../models/user');
var passport = require('passport');
var auth = require('../authenticate');
const cors = require('./cors');

router.use(bodyParser.json());

// GET users listing. 
router
.options('*', cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.get('/', cors.corsWithOptions, auth.verifyUser, auth.verifyAdmin, 
  function(req, res, next) 
{
  User.find({})
  .then((users => {
    res.statusCode = 200;
    res.contentType('application/json');
    res.json(users);
  }), (err) => next(err))
  .catch((err) => next(err));
});


//SIGN UP
router
.options(cors.corsWithOptions, (req, res) => { res.sendStatus(200); })
.post('/signup', cors.corsWithOptions, 
  (req, res, next) => 
{
  User.register(new User({username: req.body.username}), 
    req.body.password, (err, user) => {
    if(err) {
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.json({err: err});
    }
    else {
      if (req.body.firstname)
        user.firstname = req.body.firstname;
      if (req.body.lastname)
        user.lastname = req.body.lastname;
      user.save((err, user) => {
        if (err) {
          res.statusCode = 500;
          res.setHeader('Content-Type', 'application/json');
          res.json({err: err});
          return ;
        }
        passport.authenticate('local')(req, res, () => {
          res.statusCode = 200;
          res.setHeader('Content-Type', 'application/json');
          res.json({success: true, status: 'Registration Successful!'});
        });
      });
    }
  });
});

router
.post('/login', cors.corsWithOptions, (req, res, next) => 
{
  passport.authenticate('local', (err, user, info) => {
    //Info has details on why login failed
    if (err) { return next(err) }

    //Wrong input info
    if (!user) {
      res.statusCode = 401;
      res.contentType('application/json');
      return res.json({success: false, status: 'JWT invalid', err: info});
    }

    //Actual error
    req.logIn(user, (err) => {
      if(err) {
        res.statusCode = 401;
        res.contentType('application/json');
        res.json({success: false, status: 'Login Unsuccessful!', 
          err: 'Could not login user'});
          return;
      }

      var token = auth.getToken({_id: req.user._id});
      res.statusCode = 200;
      res.contentType('application/json');
      res.json({success: true, status: 'Login Successful!', token: token});
    });
  })(req, res, next);
});

router.get('/logout', cors.corsWithOptions, (req, res, next) => {
  if (req.session){
    req.session.destroy();
    res.clearCookie('session-id');
    res.redirect('/');
  } 
  else {
    var err = new Error('You are not logged in');
    err.statusCode = 403;
    next(err);
  }
})

router.get('/facebook/token', passport.authenticate('facebook-token'), (req, res) => {
  if (req.user) {
    var token = auth.getToken({_id: req.user._id});
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.json({success: true, token: token, status: 'You are successfully logged in!'});
  }
});

//Used to make sure token is still valid
router.get('/checkJWTToken', cors.corsWithOptions, (req, res) => {
  passport.authenticate('jwt', {session: false}, (err, user, info) => {
    if (err) return next(err);
    if(!user){
      res.statusCode = 401;
      res.contentType('application/json');
      return res.json({status: 'JWT invalid!', success: false, err: info});
    } 
    else {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      return res.json({status: 'JWT valid!', success: true, user: user});
    }
  }) (req, res);
});

module.exports = router;