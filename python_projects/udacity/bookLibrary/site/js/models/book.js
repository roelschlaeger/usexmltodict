// site/js/models/book.js

"use strict";

var app = app || {};

app.Book = Backbone.Model.extend({
    defaults: {
        coverImage: 'img/placeholder.png',
        title: 'No title',
        author: 'Unknown',
        releaseDate: 'Unknown',
        keywords: 'None',
    },
    parse: function(response) {
        response.id = response._id;
        return response;
    }
});
