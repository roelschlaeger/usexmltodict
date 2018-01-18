#! /bin/bash
python directions.py > test.html
tidy -i -f tidy_errors.txt test.html > test2.html
echo "Output is in test2.html"
# cat tidy_errors.txt
