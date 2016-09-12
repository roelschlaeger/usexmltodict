// Module dependencies.
// Rewritten for express 4.x based on https://expressjs.com/en/guide/migrating-4.html
var application_root = __dirname,
    mongoose = require('mongoose'), //MongoDB integration

    express = require('express'), //Web framework
    path = require('path'), //Utilities for dealing with file paths

    favicon = require('serve-favicon'),
    logger = require('morgan'),
    methodOverride = require('method-override'), //added method-override for express 4.0+
    session = require('express-session'),
    bodyParser = require('body-parser'), //Parser for reading request body
    errorHandler = require('errorhandler'),
    serveStatic = require('serve-static');

//Create server
var app = express();
var port = 4711; //default port

app.set('port', process.env.PORT || port); //default port
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');
app.use(favicon(__dirname + '/site/favicon.ico'));
app.use(logger('dev'));
app.use(methodOverride());
app.use(session({
    resave: true,
    saveUninitialized: true,
    secret: 'uwotm8'
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
// app.use(express.static(path.join(__dirname, 'site')));
app.use(
    serveStatic(
        path.join(__dirname, 'site'), {
            cacheControl: true,
            maxAge: '0d'
        }
    ));

// handles anything, for testing only
var DEBUG = false;
if (DEBUG) {
    app.use(function(req, res) {
        res.setHeader('Content-Type', 'text/plain')
        res.write('you posted:\n')
        res.end(JSON.stringify(req.body, null, 2))
    });
};

// MongoDB interface
// Use bluebird for promises
mongoose.Promise = require('bluebird');
mongoose.connect('mongodb://localhost/library_database'); //Connect to database

//Schemas
var Keywords = new mongoose.Schema({
    keyword: String
});

var Book = new mongoose.Schema({
    title: String,
    author: String,
    releaseDate: Date,
    keywords: [Keywords]
});

//Schemas
var Keywords = new mongoose.Schema({
    keyword: String
});

//Models
var BookModel = mongoose.model('Book', Book);

// Route handlers
// /api
var running = function(request, response) {
    response.send('Library API is running');
};

// Get a list of all books
// get /api/books
var getBooks = function(request, response) {
    return BookModel.find(function(err, books) {
        if (!err) {
            return response.send(books);
        } else {
            return console.log(err);
        }
    });
};

//Insert a new book
// post /api/books
// var insertBook = function(request, response) {
//     console.log("app.post(/api/books)");
//     if (request.body === undefined) {
//         console.log("request.body === undefined");
//     } else {
//         var book = new BookModel({
//             title: request.body.title,
//             author: request.body.author,
//             releaseDate: request.body.releaseDate
//         });
//
//         return book.save(function(err) {
//             if (!err) {
//                 console.log('created');
//                 return response.send(book);
//             } else {
//                 console.log(err);
//             }
//         });
//     }
// };

// Routes
// app.get('/', routes.index);
// app.get('/users', user.list);

app.get('/api', running);

//New router function for 4.0
app.route('/api/books')
    .get(getBooks) //Get a list of all books
    .post(function(request, response) { //Insert a new book
        var book = new BookModel({
            title: request.body.title,
            author: request.body.author,
            releaseDate: request.body.releaseDate,
            keywords: request.body.keywords // NEW
        });
        book.save(function(err) {
            if (!err) {
                console.log('created');
                return response.send(book);
            } else {
                return console.log(err);
            }
        });
    });

app.route('/api/books/:id')
    .put(function(request, response) { //Update a book
        console.log('Updating book ' + request.body.title);
        return BookModel.findById(request.params.id, function(err, book) {
            book.title = request.body.title;
            book.author = request.body.author;
            book.releaseDate = request.body.releaseDate;
            book.keywords = request.body.keywords; // NEW

            return book.save(function(err) {
                if (!err) {
                    console.log('book updated');
                } else {
                    console.log(err);
                }
                return response.send(book);
            });
        });
    })
    .get(function(request, response) { //Get a single book by id
        return BookModel.findById(request.params.id, function(err, book) {
            if (!err) {
                return response.send(book);
            } else {
                return console.log(err);
            }
        });
    })
    .put(function(request, response) { //Update a book
        console.log('Updating book ' + request.body.title);
        return BookModel.findById(request.params.id, function(err, book) {
            book.title = request.body.title;
            book.author = request.body.author;
            book.releaseDate = request.body.releaseDate;

            return book.save(function(err) {
                if (!err) {
                    console.log('book updated');
                    return response.send(book);
                } else {
                    console.log(err);
                }
            });
        });
    })
    .delete(function(request, response) { //Delete a book
        console.log('Deleting book with id: ' + request.params.id);
        return BookModel.findById(request.params.id, function(err, book) {
            return book.remove(function(err) {
                if (!err) {
                    console.log('Book removed');
                    return response.send('');
                } else {
                    console.log(err);
                }
            });
        });
    });

// ///////////////////////////////////////////////////////////////////////////

// SHOULD BE LOADED AFTER LOADING THE ROUTES
// error handling middleware
// console.log("app.get('env')", app.get('env'));
if ('development' === app.get('env')) {
    //Show all errors in development
    app.use(errorHandler({
        dumpExceptions: true,
        showStack: true
    }));
}

//Start server
app.disable('etag'); //http://stackoverflow.com/questions/18811286/nodejs-express-cache-and-304-status-code

app.listen(app.get('port'), function() {
    console.log(
        'Express server listening on port %d in %s mode',
        app.get('port'),
        app.settings.env
    );
});
