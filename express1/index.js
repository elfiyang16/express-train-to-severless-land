'use strict';

const serverless = require('serverless-http');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.locals.pretty = true;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.set('json spaces', 2); 

app.get('/:hash?', (req, res) => {
    let path = req.path;
    let { params, query, body } = req;

    res.status(200).send({
        status: res.statusCode,
        data: null,
        message: `${req.method} :hash - ${path}`,
        params: params,
        query: query
    })
})


/* ** ** ** ** ** ** **
* Error handling
* ** ** ** ** ** ** **/
app.use((err, req, res, next) => {
    console.error(err);
    res.status(404).json({
        status: res.statusCode,
        data: err.message,
        message: 'Not Found'
    });
});


// Development error handler will print stacktrace
if (app.get('env') === 'development') {
    app.use((err, req, res, next) => {
        res.status(err.status || 500);
        res.json({
            stage: "development",
            status: res.status,
            data: null,
            message: err.message
        });
    });
}


// Production error handler no stacktraces leaked to user
// You must provide four arguments to identify it as an error-handling middleware function.
app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({
        status: res.statusCode,
        data: err.message,
        message: 'Internal Error'
    });
});

module.exports.handler = serverless(app);