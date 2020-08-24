var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var passportLocalMongoose = require('passport-local-mongoose');

var User = new Schema({
    //User and pword automatically added by plugin passport
    //Password and user stored as hash
    firstname: {
        type: String,
        //required: true,
        default: ''
    },
    lastname: {
        type: String,
        //required: true,
        default: ''
    },
    facebookId: {
        type: String
    },
    admin:   {
        type: Boolean,
        default: false
    }
});

User.plugin(passportLocalMongoose);

module.exports = mongoose.model('User', User);