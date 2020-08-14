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

    Dishes.create({
        name: 'Uthappizza',
        description: 'test'
    })
    .then((dish) => {
        console.log(dish + '\n');

        return Dishes.findByIdAndUpdate(dish._id, {
            $set: { description: 'Updated test'}
        },{ 
            new: true 
        })
        .exec();
    })
    .then((dish) => {
        console.log(dish + '\n');

        dish.comments.push({
            rating: 5,
            comment: 'I\'m getting a sinking feeling!',
            author: 'Leonardo di Carpaccio'
        });

        return dish.save();
    })
    .then((dish) => {
        console.log(dish) + '\n';

        return Dishes.deleteMany({});
    })
    .then(() => {
        console.log('Operations performed succesfully.\n'+
        'Closing DB connection.')

        return mongoose.connection.close();
    })
    .catch((err) => {
        console.log(err);
    });

});