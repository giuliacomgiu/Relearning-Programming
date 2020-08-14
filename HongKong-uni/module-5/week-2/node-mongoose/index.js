const mongoose = require('mongoose');

const Dishes = require('./models/dishes');

//Adjusting to MongoDB + NodeJS updates
mongoose.set('useNewUrlParser', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useUnifiedTopology', true);
mongoose.set('useCreateIndex', true);

const url = 'mongodb://localhost:27017/conFusion';
const connect = mongoose.connect(url, 
    { useNewUrlParser: true }
    );

connect.then((db) => {

    console.log('Connected correctly to server\n');

    var newDish = Dishes({
        name: 'Uthappizza',
        description: 'test'
    });

    newDish.save()
        .then((dish) => {
            console.log(dish + '\n');

            return Dishes.find({});
        })
        .then((dishes) => {
            console.log(dishes + '\n');

            return Dishes.deleteMany({});
        })
        .then(() => {
            console.log('Dishes were succefully deleted\n');

            return mongoose.connection.close();
        })
        .catch((err) => {
            console.log(err);
        });

});