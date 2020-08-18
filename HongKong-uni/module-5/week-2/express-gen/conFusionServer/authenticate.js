var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var User = require('./models/user');

//User.authenticate is supplied by passport-local-mongoose
//Otherwise, we'd have to supply the auth funct
exports.local = passport.use(new LocalStrategy(User.authenticate()));

//Support for sessions
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());