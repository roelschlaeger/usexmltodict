*********
bob_notes
*********

:author: Robert L. Oelschlaeger
:date: 20141129

Running `Node.js tutorial for beginners`_, stopped at about 06:18.

.. _`Node.js tutorial for beginners`: https://www.youtube.com/watch?v=FqMIyTH9wSg&src_vid=ndKRjmA6WNA&feature=iv&annotation_id=annotation_2934154685

Completed generation of ``exp2014`` using alternative for Jade.

.. code:: bash

    node -v
    npm -v
    npm install -g express-generator
    express exp2014 --hogan -c less
    cd exp2014
    npm install

Then, to run the application we could have done

.. code:: bash

    node bin/www

but, instead of having to stop and restart the application, we installed ``nodemon`` instead, which will take care of stopping and restarting the application when the source files are changed:

.. code:: bash

    npm install -g nodemon
    nodemon bin/www

