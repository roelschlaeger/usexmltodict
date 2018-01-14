#! /bin/bash
python directions.py > test.html
tidy -i -f tidy_errors.txt test.html > test2.html
# cat tidy_errors.txt
