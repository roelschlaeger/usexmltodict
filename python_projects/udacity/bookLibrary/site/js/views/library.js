// site/js/views/library.js

"use strict";

var app = app || {};

app.LibraryView = Backbone.View.extend({

    el: '#books',

    events: {
        'click #add': 'addBook'
    },

    initialize: function(initialBooks) {
        this.collection = new app.Library(initialBooks);
        this.listenTo( this.collection, 'add', this.renderBook );
        this.render();
    },

    // render library by rendering each book in its collection
    render: function() {
        this.collection.each(function(item) {
            this.renderBook(item);
        }, this);
    },

    // render a book by creating a BookView and appending the
    // element it renders to the library's element
    renderBook: function(item) {
        var bookView = new app.BookView({
            model: item
        });
        this.$el.append(bookView.render().el);
    },

    addBook: function(e) {
        // console.log("addBook");

        e.preventDefault();

        var formData = {};

        $('#addBook div').children('input').each(function(i, el) {
            if ($(el).val() !== '') {
                formData[el.id] = $(el).val();
            }
            // console.log(formData);
            if(formData.coverImage !== undefined) {
                console.log(formData.coverImage);
                // console.log(window.location.pathname);
            }

        });

        // :console.log(formData);
        this.collection.add(new app.Book(formData));
    }

});
