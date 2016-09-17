// site/js/views/book.js

"use strict";

var app = app || {};

app.BookView = Backbone.View.extend({
    tagName: 'div',

    className: 'bookContainer',

    template: _.template($('#bookTemplate').html()),

    events: {
        'click .delete': 'deleteBook'
    },

    initialize: function(args) {
        _.bindAll(this, "deleteBook", "render");

        this.listenTo(this, "click .delete", this.deleteBook);
    },

    deleteBook: function() {
        console.log("deleteBook", this, this.model, this.model.destroy);

        //Delete model
        this.model.destroy();

        //Delete view
        this.remove();
    },

    render: function() {
        //this.el is what we defined in tagName. use $el to get access to jQuery html() function
        this.$el.html(this.template(this.model.attributes));

        return this;
    }
});
