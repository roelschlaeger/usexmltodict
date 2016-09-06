// site/js/collections/library.js

"use strict";

var app = app || {};

app.Library = Backbone.Collection.extend({
    model: app.Book
});
